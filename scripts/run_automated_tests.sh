
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${PYTHON_BIN:-.venv/bin/python}"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Python executable not found: $PYTHON_BIN"
  echo "Set PYTHON_BIN or create virtual env at .venv"
  exit 1
fi

echo "[1/2] Running integration tests..."
"$PYTHON_BIN" manage.py test tests.integration -v 2

echo "[2/2] Running security tests..."
"$PYTHON_BIN" manage.py test tests.security -v 2

echo "Automated tests completed successfully."
