import sys
import os
import questionary
from src.detectors import URLDetector
from src.youtube import YouTubeHandler
from src.spotify import SpotifyHandler
from src.ui import UI
from src.config import ConfigManager

def main():
    UI.show_banner()
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # Fallback to asking user if no arg provided
        url = questionary.text("Paste URL here:").ask()

    if not url:
        print("No URL provided.")
        return

    source = URLDetector.detect(url)
    UI.show_message(f"Detected Source: [bold cyan]{source.upper()}[/bold cyan]")

    if source == 'youtube':
        process_youtube(url)

    elif source == 'spotify':
        process_spotify(url)
        
    elif source == 'search':
        handler = YouTubeHandler()
        results = handler.search(url, limit=10)
        
        if not results:
            UI.show_message("No results found.", style="bold red")
            return

        # Create choices for selection
        choices = []
        for entry in results:
            title = entry.get('title', 'Unknown')
            uploader = entry.get('uploader', 'Unknown')
            duration = entry.get('duration_string', 'N/A')
            choices.append(questionary.Choice(
                title=f"{title} ({duration}) - {uploader}",
                value=entry.get('webpage_url') or entry.get('url')
            ))
        choices.append(questionary.Choice(title="Cancel", value=None))

        selected_url = questionary.select(
            "Select a video to download:",
            choices=choices
        ).ask()

        if selected_url:
            process_youtube(selected_url)
        else:
            print("Aborted.")

    else:
        UI.show_message("Unsupported input detected.", style="bold red")

def process_youtube(url):
    handler = YouTubeHandler()
    info = handler.get_info(url)
    
    if info:
        UI.show_info(info)
        
        while True:
            main_choices = [
                questionary.Choice(title="Download Video", value="video"),
                questionary.Choice(title="Download Audio", value="audio"),
                questionary.Choice(title="Cancel", value="cancel")
            ]
            
            main_choice = UI.ask_action(main_choices)
            
            if main_choice == "video":
                # Fetch available resolutions
                resolutions = handler.get_available_resolutions(info.get('formats', []))
                
                if not resolutions:
                    # Fallback if parsing fails
                    handler.download_video(url)
                    return

                # Create resolution choices
                res_choices = [questionary.Choice(title="Best Available", value="best")]
                for res in resolutions:
                    res_choices.append(questionary.Choice(title=f"{res}p", value=res))
                
                res_choices.append(questionary.Choice(title="Back", value="back"))
                res_choices.append(questionary.Choice(title="Cancel", value="cancel"))
                
                res_choice = UI.ask_list("Select Resolution:", res_choices)
                
                if res_choice == "back":
                    continue
                elif res_choice == "cancel":
                    print("Aborted.")
                    return
                elif res_choice == "best":
                    handler.download_video(url)
                    return
                else:
                    handler.download_video(url, height=res_choice)
                    return

            elif main_choice == "audio":
                audio_choices = [
                    questionary.Choice(title="MP3 (Universal)", value="mp3"),
                    questionary.Choice(title="M4A (Better Quality)", value="m4a"),
                    questionary.Choice(title="FLAC (Lossless)", value="flac"),
                    questionary.Choice(title="WAV (Uncompressed)", value="wav"),
                    questionary.Choice(title="OPUS (High Efficiency)", value="opus"),
                    questionary.Choice(title="Back", value="back"),
                    questionary.Choice(title="Cancel", value="cancel")
                ]
                
                fmt_choice = UI.ask_list("Select Audio Format:", audio_choices)
                
                if fmt_choice == "back":
                    continue
                elif fmt_choice == "cancel":
                    print("Aborted.")
                    return
                else:
                    handler.download_audio(url, audio_format=fmt_choice)
                    return
                    
            elif main_choice == "cancel":
                print("Aborted.")
                return
    else:
        UI.show_message("Failed to fetch video info", style="bold red")

def process_spotify(url):
    # Check for credentials
    client_id, client_secret = ConfigManager.get_spotify_credentials()
    
    if not (client_id and client_secret):
        # Ask user if they want to configure them now
        should_configure = questionary.confirm(
            "Spotify credentials missing. Configure now to avoid rate limits?"
        ).ask()
        
        if should_configure:
            new_id, new_secret = UI.ask_credentials()
            if new_id and new_secret:
                ConfigManager.save_config({
                    'spotify_client_id': new_id,
                    'spotify_client_secret': new_secret
                })
                UI.show_message("Credentials saved!", style="green")

    handler = SpotifyHandler()
    # SpotDL is self-contained, so we just ask to confirm
    choices = [
        "Download",
        "Cancel"
    ]
    choice = UI.ask_action(choices)
    if choice == "Download":
        handler.download(url)
    else:
        print("Aborted.")

if __name__ == "__main__":
    main()
