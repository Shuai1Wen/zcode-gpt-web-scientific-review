---
description: Initialize the GPT Web scientific-review coordinator and configure the two interleaved hourly ZCode heartbeat tasks used for Pro runs.
argument-hint: "[optional project note]"
skills: gpt-web-orchestrator, gpt-web-browser, gpt-pro-watch
disable-noninteractive: true
---

Initialize this local ZCode project for GPT Web Scientific Review.

$ARGUMENTS

Perform these steps:

1. Create `.gpt-web-review/coordinator.json` if absent. It must contain coordination metadata only, never credentials.
2. Confirm ZCode's official Browser Automation/Browser Use capability is enabled.
3. Open ChatGPT Web in the ZCode built-in browser. If login/security verification is needed, stop and ask the user to complete it manually.
4. Ask the user to enable ZCode Automations **Keep awake** for long Pro runs.
5. Configure two scheduled tasks bound to this coordinator session when ZCode exposes scheduled-task creation from chat:

   **Task A — GPT Pro heartbeat :00**
   - Frequency: Hourly
   - Minute: 00
   - Instructions: "Run the gpt-pro-watch heartbeat for the active `.gpt-web-review` Pro job in this session. Read and inspect only. If no active Pro job exists, report NO_ACTIVE_PRO_JOB. Never send a ChatGPT message, retry, refresh due only to time, switch model, or create a new job."

   **Task B — GPT Pro heartbeat :30**
   - Frequency: Hourly
   - Minute: 30
   - Same instructions.

6. Use read-only/lowest-change permissions for heartbeat tasks. Keep the model/thought settings at the project's normal level; heartbeat reasoning itself does not need Pro.
7. If the current ZCode build does not expose task creation from this command/session, do not claim success. Instead print the two exact task definitions above so the user can create them on the Automations page.
8. Do not create more than these two recurring heartbeat tasks. They are shared by all Pro review jobs in this coordinator session.

Finish with a setup report containing: browser login status, coordinator path, Keep awake reminder, Task A status, Task B status, and whether Pro review is ready.
