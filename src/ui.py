from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.align import Align
from rich import box
import questionary

console = Console()

class UI:
    @staticmethod
    def show_banner():
        console.clear()
        # ASCII Art Title
        ascii_title = """
██╗   ██╗ ██████╗ ██╗   ██╗███████╗██╗   ██╗
╚██╗ ██╔╝██╔═══██╗██║   ██║██╔════╝╚██╗ ██╔╝
 ╚████╔╝ ██║   ██║██║   ██║█████╗   ╚████╔╝ 
  ╚██╔╝  ██║   ██║██║   ██║██╔══╝    ╚██╔╝  
   ██║   ╚██████╔╝╚██████╔╝██║        ██║   
   ╚═╝    ╚═════╝  ╚═════╝ ╚═╝        ╚═╝   
        """
        title = Text(ascii_title, style="bold green")
        subtitle = Text("YouTube & Spotify Downloader", style="italic white")
        
        content = Align.center(Text.assemble(title, "\n", subtitle))
        panel = Panel(content, border_style="green", box=box.ROUNDED)
        console.print(panel)

    @staticmethod
    def show_info(info):
        table = Table(show_header=False, box=box.SIMPLE_HEAD, border_style="bright_blue")
        table.add_column("Key", style="bold cyan")
        table.add_column("Value", style="white")

        table.add_row("Title", info.get('title', 'Unknown'))
        table.add_row("Uploader/Artist", info.get('uploader', 'Unknown'))
        
        if info.get('duration'):
            mins, secs = divmod(info['duration'], 60)
            duration_str = f"{int(mins)}m {int(secs)}s"
            table.add_row("Duration", duration_str)
            
        if info.get('view_count'):
            table.add_row("Views", f"{info['view_count']:,}")

        panel = Panel(
            table, 
            title="[bold green]Media Information[/bold green]",
            border_style="green",
            box=box.ROUNDED,
            expand=False
        )
        console.print(panel)

    @staticmethod
    def ask_action(actions):
        return questionary.select(
            "Select Action:",
            choices=actions,
            qmark="?",
            pointer="❯",
            style=questionary.Style([
                ('qmark', 'fg:purple bold'),
                ('question', 'fg:white bold'),
                ('answer', 'fg:cyan bold'),
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan bold'),
                ('selected', 'fg:cyan bold'),
                ('separator', 'fg:grey'),
                ('instruction', 'fg:grey italic'),
            ])
        ).ask()
    
    @staticmethod
    def ask_list(message, choices):
        return questionary.select(
            message,
            choices=choices,
            qmark="?",
            pointer="❯",
            style=questionary.Style([
                ('qmark', 'fg:purple bold'),
                ('question', 'fg:white bold'),
                ('answer', 'fg:cyan bold'),
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan bold'),
                ('selected', 'fg:cyan bold'),
                ('separator', 'fg:grey'),
                ('instruction', 'fg:grey italic'),
            ])
        ).ask()
    
    @staticmethod
    def show_message(msg, style="bold green"):
        console.print(msg, style=style)

    @staticmethod
    def ask_credentials():
        console.print(Panel("[yellow]Spotify credentials are required to avoid rate limits.[/yellow]", title="Authentication", border_style="yellow"))
        client_id = questionary.password("Enter Spotify Client ID:").ask()
        client_secret = questionary.password("Enter Spotify Client Secret:").ask()
        return client_id, client_secret
