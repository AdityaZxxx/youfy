# Spotube - Spotify & YouTube Downloader

A beautiful, CLI-based media downloader for Linux.

## Features
- **Auto-Detect:** Paste a YouTube or Spotify link, and it knows what to do.
- **YouTube:** Download Video (Best/1080p) or Audio (MP3).
- **Spotify:** Download tracks or playlists (using YouTube source matching).
- **Aesthetic UI:** Built with `rich` for a modern terminal experience.
- **Portable:** Configuration stored in `~/.config/spotube`.

## Installation

1. Clone or download this repository.
2. Run the setup script:
   ```bash
   ./setup.sh
   ```

## Usage

Run the tool:
```bash
./run.sh
```

Or paste a URL directly:
```bash
./run.sh "https://youtube.com/watch?v=..."
```

## Configuration

On first run with a Spotify link, you will be asked for your Spotify Client ID and Secret to avoid rate limits. These are stored in `~/.config/spotube/config.json`.
