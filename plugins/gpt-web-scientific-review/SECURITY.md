# Security and account-safety notes

This plugin is intentionally designed without credential handling.

## Never store

- ChatGPT password
- cookies
- session tokens
- authentication headers
- 2FA/TOTP seeds or recovery codes
- browser profile exports

Authentication is performed manually in ZCode's built-in browser.

## Browser actions that require human intervention

If login, CAPTCHA, 2FA, account verification, payment, or another security challenge appears, set the job to `AUTH_REQUIRED` and stop automated interaction until the user completes it.

## No bypass behavior

The workflow must not rotate accounts, evade rate limits, bypass access controls, defeat anti-bot measures, or convert ChatGPT Web into a high-throughput unofficial API.
