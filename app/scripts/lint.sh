#!/usr/bin/env bash
set -euo pipefail
black . && isort . && flake8 .
