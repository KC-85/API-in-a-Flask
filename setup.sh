#!/usr/bin/env bash
set -euo pipefail

echo "Updating system and installing dependencies..."
if command -v apt >/dev/null 2>&1; then
  sudo apt update
  sudo apt install -y redis-server python3-pip python3-venv
elif command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y redis python3-pip
else
  echo "Unsupported package manager. Install Redis and python3-pip manually." >&2
  exit 1
fi

echo "Starting Redis server..."
if command -v systemctl >/dev/null 2>&1; then
  if systemctl list-unit-files | grep -q '^redis\.service'; then
    sudo systemctl enable --now redis
  elif systemctl list-unit-files | grep -q '^redis-server\.service'; then
    sudo systemctl enable --now redis-server
  else
    redis-server --daemonize yes
  fi
else
  redis-server --daemonize yes
fi

echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

if [[ ! -f .env ]]; then
  echo "Creating .env with local seed credentials..."
  cat > .env << 'EOF'
SEED_ADMIN_PASSWORD=adminpass
SEED_USER_PASSWORD=johnpass
EOF
fi

echo "Running tests..."
pytest -v

echo "Setup complete!"
