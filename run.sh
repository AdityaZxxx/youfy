#!/bin/bash
# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Activate venv from the script directory
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
else
    echo "Error: Virtual environment not found in $SCRIPT_DIR/venv"
    echo "Please run ./setup.sh first."
    exit 1
fi

# Run main.py from the script directory
# Also add SCRIPT_DIR to PYTHONPATH so imports work correctly
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
python "$SCRIPT_DIR/main.py" "$@"
