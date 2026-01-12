#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Spotube Setup (Spotify & YouTube Downloader) ===${NC}"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 could not be found."
    exit 1
fi

# Check for FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "Warning: FFmpeg is not installed. Some features might not work."
    echo "Please install it using your package manager (e.g., sudo apt install ffmpeg)."
fi

# Create Virtual Environment
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv "$SCRIPT_DIR/venv"
fi

# Install Dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
"$SCRIPT_DIR/venv/bin/pip" install -U pip
"$SCRIPT_DIR/venv/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"

# Make run script executable
chmod +x "$SCRIPT_DIR/run.sh"

echo -e "${GREEN}Setup Complete!${NC}"
echo -e "You can now run the tool using: ${BLUE}./run.sh${NC}"
echo -e "Or create a symlink to use it globally:"
echo -e "  sudo ln -s $SCRIPT_DIR/run.sh /usr/local/bin/media-cli"
