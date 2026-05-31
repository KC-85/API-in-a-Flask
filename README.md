# API in a Flask
Personal project - Wanted to see if i could build a RestAPI using Flask (Python)

## set_env.sh (helper)

This repo includes a small helper script, [set_env.sh](set_env.sh), which fetches a JWT from the local running API and helps you export it or save it to a local `.env` file.

- Requirements: `curl` and `jq` installed.
- To write the token to `.env` interactively (recommended if you want a file):

```bash
./set_env.sh
# answer 'y' when prompted to save to .env
```

- To export the token into your current shell without persisting to disk:

```bash
eval "$(./set_env.sh export)"
```

- Security: `.env` is ignored by default; do not commit it. Tokens are secrets — prefer ephemeral exports or a secrets manager for automation.

