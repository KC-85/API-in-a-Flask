#!/usr/bin/env bash
set -euo pipefail

# Safe helper: fetch a JWT token and either export it or write to .env (opt-in)
# Usage: ./set_env.sh

if ! command -v curl >/dev/null 2>&1; then
     echo "curl is required but not found" >&2
     exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
     echo "jq is required but not found. Install it or modify the script to parse JSON differently." >&2
     exit 1
fi

TOKEN=$(curl -s -X POST http://127.0.0.1:8080/auth/login \
     -H "Content-Type: application/json" \
     -d "{\"username\": \"admin\", \"password\": \"${SEED_ADMIN_PASSWORD:-adminpass}\"}" | jq -r .access_token)

if [[ -z "$TOKEN" || "$TOKEN" == "null" ]]; then
     echo "Failed to fetch token" >&2
     exit 1
fi

echo "Token fetched. Do you want to save it to .env? [y/N]"
read -r answer || true

if [[ "$answer" =~ ^[Yy]$ ]]; then
     printf "JWT_TOKEN=%s\n" "$TOKEN" > .env
     echo ".env written (ensure it's in .gitignore)"
else
     # Source in current shell won't persist unless user `eval`s the output.
     # Print an export line so the user can `eval $(./set_env.sh)` if they want to export.
     echo "# To export into current shell: run -> eval \"$(pwd)/set_env.sh export\""
     echo "JWT_TOKEN=$TOKEN"
fi

if [[ ${1-} == "export" ]]; then
     # Helpful mode: prints an export command which can be eval'd by caller
     printf "export JWT_TOKEN=%q\n" "$TOKEN"
fi
