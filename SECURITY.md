# Security policy

## Reporting a vulnerability

Do not publish credentials, bot tokens, private recordings, or exploit details in a public issue. Report security concerns privately to the repository owner through the GitHub security contact available to the project account.

## Sensitive material

Never commit `.env` files, tokens, private keys, camera credentials, datasets containing personal data, recordings, local event databases, or model weights without an explicit review. The repository ignore rules cover common cases, but inspect `git diff --cached` before every commit.

## Deployment baseline

Keep the dashboard bound to localhost or a protected private network. Use HTTPS and authentication before exposing it beyond a trusted network. Treat Telegram bot tokens as passwords and rotate them if exposure is suspected.
