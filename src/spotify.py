import subprocess
import os
from src.config import ConfigManager
from rich.console import Console

console = Console()

class SpotifyHandler:
    def __init__(self, output_dir=None):
        if output_dir is None:
            # Default to User's Music folder for Spotify
            self.output_dir = os.path.expanduser("~/Downloads/Youfy/Spotify")
        else:
            self.output_dir = output_dir
            
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def download(self, url):
        client_id, client_secret = ConfigManager.get_spotify_credentials()
        
        # Base command
        cmd = ["spotdl", "download", url, "--output", self.output_dir]
        
        # Add auth if available
        if client_id and client_secret:
            cmd.extend([
                "--client-id", client_id, 
                "--client-secret", client_secret,
                "--no-cache",
                "--headless"
            ])
        else:
            console.print("[yellow]Warning: No Spotify credentials found. You might hit rate limits.[/yellow]")
            console.print("Run the tool again and look for a configuration option or just add them when prompted.")

        console.print(f"[bold cyan]Starting Spotify Download for:[/bold cyan] {url}")
        console.print(f"[cyan]Saving to:[/cyan] {self.output_dir}")
        
        try:
            subprocess.run(cmd, check=True)
            console.print(f"\n[bold green]Done![/bold green] File saved in: {self.output_dir}")
        except subprocess.CalledProcessError as e:
            console.print(f"[bold red]Error downloading:[/bold red] {e}")
            if not (client_id and client_secret):
                 console.print("[bold red]Tip:[/bold red] This error might be due to rate limits. Configure your Client ID/Secret.")
        except FileNotFoundError:
            console.print("[bold red]Error:[/bold red] spotdl command not found. Make sure it is installed.")

