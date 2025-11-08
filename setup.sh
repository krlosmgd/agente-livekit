#!/usr/bin/env bash
set -euo pipefail

echo "[setup] Creating virtual environment .venv (requires Python >= 3.13)"
python3 -m venv .venv

echo "[setup] Activating virtual environment and upgrading pip"
# shellcheck disable=SC1091
. .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel

echo "[setup] Installing dependencies from requirements.txt"
pip install -r requirements.txt

echo "\n[setup] Installation complete. To start using the environment run:\n"
echo "  source .venv/bin/activate"
echo "  python3 run_agent.py"

echo "If you prefer to install from the project package (editable mode):"
echo "  python -m pip install -e ."
