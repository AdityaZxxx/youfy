# Youfy - YouTube & Spotify Downloader

A beautiful, advanced CLI-based media downloader for Linux. Built for productivity nerds who love their terminal.

## Features

- **Smart Search:** No need for links! Just type `./run.sh "song name"` and pick from the results.
- **Dynamic Video Quality:** Choose from all available resolutions (4K, 1440p, 1080p, 720p, etc.) or just grab the "Best Available".
- **Pro Audio Formats:** Support for **MP3, M4A, FLAC (Lossless), WAV, and OPUS**.
- **Meta-Tagged:** Automatically embeds album art (thumbnails) and metadata into your MP3/FLAC files.
- **Spotify & YouTube:** Auto-detects links. Downloads Spotify tracks/playlists via YouTube matching.
- **Aesthetic UI:** Beautiful terminal interface with live progress bars, spinners, and ASCII art.
- **Rate Limit Safe:** configurable Spotify credentials to avoid API limits.

## Installation

1. Clone this repository:
   ```bash
   git clone <your-repo-url> youfy
   cd youfy
   ```
2. Run the setup script:
   ```bash
   ./setup.sh
   ```
   *This will create a virtual environment and install all dependencies.*

3. (Optional) Create a global symlink:
   ```bash
   sudo ln -s $(pwd)/run.sh /usr/local/bin/youfy
   ```
   *Now you can run `youfy` from anywhere!*

## Usage Examples

### 1. Interactive Mode
Just run the tool and it will ask you what to do.
```bash
./run.sh
# or if you symlinked it:
youfy
```

### 2. Search & Download (Best Feature!)
Search for a video or song directly from the command line.
```bash
./run.sh "lofi girl hip hop radio"
```
*You will see a list of results. Select one, then choose Video or Audio format.*

### 3. Download from URL
Paste a YouTube or Spotify link directly.

**YouTube:**
```bash
./run.sh "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```
*Menu Options: Download Video (Select Resolution) / Download Audio (Select Format)*

**Spotify:**
```bash
./run.sh "https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT"
```
*Downloads the track (or playlist) automatically.*

## Configuration

### Spotify Credentials
To avoid rate limits (429 Too Many Requests) when downloading from Spotify, you need to provide your own Client ID and Secret.
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
2. Create a new app (name it anything).
3. Run Youfy with a Spotify link for the first time.
4. Paste your **Client ID** and **Client Secret** when prompted.

Configuration is stored securely in `~/.config/youfy/config.json`.

## Supported Formats
- **Audio:** MP3, M4A, FLAC, WAV, OPUS.
- **Video:** MP4 (h.264/h.265) - Auto merges best video+audio streams.

## License
MIT License
