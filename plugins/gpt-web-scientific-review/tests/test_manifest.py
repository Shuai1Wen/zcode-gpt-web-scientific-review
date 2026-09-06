import json
import re
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
MARKET = PLUGIN.parent.parent


class ManifestTests(unittest.TestCase):
    def test_plugin_manifest(self):
        data = json.loads((PLUGIN / '.zcode-plugin' / 'plugin.json').read_text(encoding='utf-8'))
        self.assertRegex(data['name'], r'^[a-z0-9][a-z0-9._-]{0,127}$')
        self.assertEqual(data['commands'], 'commands')
        self.assertEqual(data['skills'], 'skills')

    def test_marketplace_version_matches(self):
        plugin = json.loads((PLUGIN / '.zcode-plugin' / 'plugin.json').read_text(encoding='utf-8'))
        market = json.loads((MARKET / 'marketplace.json').read_text(encoding='utf-8'))
        entry = next(x for x in market['plugins'] if x['name'] == plugin['name'])
        self.assertEqual(entry['version'], plugin['version'])

    def test_skill_flat_layout_and_frontmatter(self):
        skill_dirs = sorted((PLUGIN / 'skills').iterdir())
        self.assertEqual(len(skill_dirs), 5)
        for d in skill_dirs:
            self.assertTrue(d.is_dir())
            text = (d / 'SKILL.md').read_text(encoding='utf-8')
            self.assertTrue(text.startswith('---\n'))
            self.assertIn(f'name: {d.name}', text)
            self.assertIn('description:', text)
            self.assertLessEqual(len((d / 'SKILL.md').read_bytes()), 100 * 1024)

    def test_command_names(self):
        command_re = re.compile(r'^[a-z0-9][a-z0-9_:-]{0,63}$')
        commands = sorted((PLUGIN / 'commands').glob('*.md'))
        self.assertEqual(len(commands), 7)
        for command in commands:
            self.assertRegex(command.stem, command_re)


if __name__ == '__main__':
    unittest.main()
