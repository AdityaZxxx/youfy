#!/bin/bash

# Resolve the true directory of the script (follow symlinks)
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do 
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" 
done
SCRIPT_DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"

# Activate venv from the script directory
if [ -f "$SCRIPT_DIR/venv/bin/activate" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
else
    echo "Error: Virtual environment not found in $SCRIPT_DIR/venv"
    echo "Please run setup.sh inside the project directory first."
    exit 1
fi

# Run main.py from the script directory
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
python "$SCRIPT_DIR/main.py" "$@"

