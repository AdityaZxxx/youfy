import yt_dlp
import os
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.console import Console

console = Console()

class QuietLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        console.print(f"[bold red]Error:[/bold red] {msg}")

class YouTubeHandler:
    def __init__(self, output_dir=None):
        if output_dir is None:
            # Default to User's Downloads folder
            self.output_dir = os.path.expanduser("~/Downloads/Spotube/YouTube")
        else:
            self.output_dir = output_dir
            
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def get_info(self, url):
        with console.status("[bold green]Fetching metadata...[/bold green]", spinner="dots"):
            ydl_opts = {
                'quiet': True, 
                'no_warnings': True,
                'logger': QuietLogger()
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(url, download=False)
                    return {
                        'title': info.get('title'),
                        'uploader': info.get('uploader'),
                        'duration': info.get('duration'),
                        'view_count': info.get('view_count'),
                        'is_playlist': 'entries' in info,
                        'playlist_count': len(info['entries']) if 'entries' in info else 0,
                        'formats': info.get('formats', [])
                    }
                except Exception as e:
                    return None

    def get_available_resolutions(self, formats):
        resolutions = set()
        for f in formats:
            if f.get('vcodec') != 'none' and f.get('height'):
                resolutions.add(f['height'])
        return sorted(list(resolutions), reverse=True)

    def search(self, query, limit=5):
        with console.status(f"[bold green]Searching for '{query}'...[/bold green]", spinner="dots"):
            ydl_opts = {
                'quiet': True, 
                'no_warnings': True,
                'extract_flat': True,
                'logger': QuietLogger()
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    # ytsearchN:query searches for N results
                    result = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
                    if 'entries' in result:
                        return result['entries']
                except Exception as e:
                    return []
        return []

    def download_video(self, url, height=None):
        if height:
            format_str = f'bestvideo[height<={height}]+bestaudio/best[height<={height}]'
        else:
            format_str = 'bestvideo+bestaudio/best'
            
        ydl_opts = {
            'format': format_str,
            'outtmpl': f'{self.output_dir}/%(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'writethumbnail': True,
            'addmetadata': True,
            'postprocessors': [
                {'key': 'EmbedThumbnail'},
                {'key': 'FFmpegMetadata'},
            ],
        }
        self._download(url, ydl_opts)

    def download_audio(self, url, audio_format='mp3'):
        # Map nice names to ffmpeg codec names/args
        # formats: mp3, m4a, flac, wav, opus
        codec_map = {
            'mp3': {'codec': 'mp3', 'quality': '192'},
            'm4a': {'codec': 'm4a', 'quality': None}, # default
            'flac': {'codec': 'flac', 'quality': None},
            'wav': {'codec': 'wav', 'quality': None},
            'opus': {'codec': 'opus', 'quality': None},
        }
        
        target = codec_map.get(audio_format, codec_map['mp3'])
        
        postprocessors = [{'key': 'FFmpegExtractAudio', 'preferredcodec': target['codec']}]
        
        if target['quality']:
             postprocessors[0]['preferredquality'] = target['quality']

        # Embedding thumbnail only works well for mp3/m4a/flac usually
        if audio_format in ['mp3', 'm4a', 'flac']:
             postprocessors.append({'key': 'EmbedThumbnail'})
             postprocessors.append({'key': 'FFmpegMetadata'})

        ydl_opts = {
            'format': 'bestaudio/best',
            'writethumbnail': True if audio_format in ['mp3', 'm4a', 'flac'] else False,
            'addmetadata': True if audio_format in ['mp3', 'm4a', 'flac'] else False,
            'postprocessors': postprocessors,
            'outtmpl': f'{self.output_dir}/%(title)s.%(ext)s',
        }
        self._download(url, ydl_opts)


    def _download(self, url, opts):
        console.print(f"\n[bold cyan]Downloading to:[/bold cyan] {self.output_dir}")
        
        # Add progress hook
        opts['progress_hooks'] = [self._progress_hook]
        opts['quiet'] = True
        opts['noprogress'] = True
        opts['logger'] = QuietLogger()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
            console=console
        ) as progress:
            self.progress_bar = progress
            self.task_id = progress.add_task("Downloading...", filename="Starting...", start=False)
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
                
        console.print(f"[bold green]Done![/bold green] File saved in: {self.output_dir}")

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            if self.task_id is not None:
                filename = os.path.basename(d.get('filename', 'Unknown'))
                # Truncate filename if too long
                if len(filename) > 30:
                    filename = filename[:27] + "..."
                
                downloaded = d.get('downloaded_bytes', 0)
                total = d.get('total_bytes', d.get('total_bytes_estimate', 0))
                
                if total > 0:
                    self.progress_bar.update(
                        self.task_id, 
                        completed=downloaded, 
                        total=total, 
                        filename=filename
                    )

        elif d['status'] == 'finished':
            self.progress_bar.update(self.task_id, filename="Processing [FFmpeg]...")
