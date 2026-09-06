import importlib.util
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / 'scripts' / 'job_state.py'
spec = importlib.util.spec_from_file_location('job_state', MODULE_PATH)
job_state = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(job_state)


class JobStateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_setup_creates_coordinator(self):
        rc = job_state.cmd_setup(Namespace(root=self.root, notes='test', force=False))
        self.assertEqual(rc, 0)
        path = self.root / '.gpt-web-review' / 'coordinator.json'
        self.assertTrue(path.exists())
        data = json.loads(path.read_text(encoding='utf-8'))
        self.assertEqual(data['heartbeat_protocol'], 'dual-hourly')
        self.assertEqual(data['heartbeat_a_minute'], 0)
        self.assertEqual(data['heartbeat_b_minute'], 30)
        self.assertTrue(data['keep_awake_required'])

    def test_new_job_and_forward_transition(self):
        rc = job_state.cmd_new(Namespace(
            root=self.root,
            topic='unseen donor review',
            mode='PRO',
            job_id='20260906_1700_unseen-donor',
            allow_fallback=False,
            force=False,
        ))
        self.assertEqual(rc, 0)
        rc = job_state.cmd_set(Namespace(
            root=self.root,
            job_id='20260906_1700_unseen-donor',
            status='PACKET_READY',
            visible_model=None,
            backend_model=None,
            temporary_chat=None,
            chat_url=None,
            note='packet written',
            force=False,
        ))
        self.assertEqual(rc, 0)
        state = json.loads(job_state.state_path(self.root, '20260906_1700_unseen-donor').read_text(encoding='utf-8'))
        self.assertEqual(state['status'], 'PACKET_READY')
        self.assertFalse(state['allow_fallback'])

    def test_backwards_transition_rejected(self):
        job_state.cmd_new(Namespace(
            root=self.root, topic='x', mode='PRO', job_id='job1',
            allow_fallback=False, force=False,
        ))
        common = dict(root=self.root, job_id='job1', visible_model=None,
                      backend_model=None, temporary_chat=None, chat_url=None,
                      note=None, force=False)
        job_state.cmd_set(Namespace(status='MODEL_SELECTED', **common))
        with self.assertRaises(SystemExit):
            job_state.cmd_set(Namespace(status='CREATED', **common))

    def test_heartbeat_marks_stall_only_after_threshold(self):
        job_state.cmd_new(Namespace(
            root=self.root, topic='x', mode='PRO', job_id='job2',
            allow_fallback=False, force=False,
        ))
        common = dict(root=self.root, job_id='job2', visible_model='Pro',
                      backend_model=None, temporary_chat='true', chat_url='https://chatgpt.com/c/test',
                      note=None, force=False)
        job_state.cmd_set(Namespace(status='RUNNING_PRO', **common))
        for _ in range(4):
            job_state.cmd_heartbeat(Namespace(
                root=self.root, job_id='job2', summary='thinking indicator visible',
                result='running', stall_threshold=4,
            ))
        state = json.loads(job_state.state_path(self.root, 'job2').read_text(encoding='utf-8'))
        # The first heartbeat establishes the baseline; four more identical summaries
        # would reach unchanged_heartbeats == 4. Here we have three unchanged comparisons.
        self.assertEqual(state['status'], 'RUNNING_PRO')
        self.assertEqual(state['unchanged_heartbeats'], 3)
        job_state.cmd_heartbeat(Namespace(
            root=self.root, job_id='job2', summary='thinking indicator visible',
            result='running', stall_threshold=4,
        ))
        state = json.loads(job_state.state_path(self.root, 'job2').read_text(encoding='utf-8'))
        self.assertEqual(state['status'], 'SUSPECTED_STALL')
        self.assertEqual(state['unchanged_heartbeats'], 4)

    def test_freeze_is_immutable_without_force(self):
        job_state.cmd_new(Namespace(
            root=self.root, topic='x', mode='EXTRA_HIGH', job_id='job3',
            allow_fallback=False, force=False,
        ))
        common = dict(root=self.root, job_id='job3', visible_model='Extra High',
                      backend_model=None, temporary_chat='true', chat_url='https://chatgpt.com/c/test',
                      note=None, force=False)
        job_state.cmd_set(Namespace(status='COMPLETED', **common))
        first = self.root / 'first.md'
        first.write_text('# raw review\nKEEP\n', encoding='utf-8')
        job_state.cmd_freeze(Namespace(root=self.root, job_id='job3', file=str(first), force=False))
        state = json.loads(job_state.state_path(self.root, 'job3').read_text(encoding='utf-8'))
        self.assertTrue(state['response_frozen'])
        self.assertEqual(state['status'], 'EXTRACTED')
        second = self.root / 'second.md'
        second.write_text('# different\nREJECT\n', encoding='utf-8')
        with self.assertRaises(SystemExit):
            job_state.cmd_freeze(Namespace(root=self.root, job_id='job3', file=str(second), force=False))

    def test_secret_field_scan(self):
        findings = job_state.scan_secrets({'safe': 1, 'session_token': 'x'})
        self.assertIn('session_token', findings)


if __name__ == '__main__':
    unittest.main()
