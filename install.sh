#!/usr/bin/env bash
set -euo pipefail
uv --version

deactivate || true
rm -rf venv || true
uv venv venv --python 3.12

source venv/bin/activate
uv pip install -r requirements.txt
