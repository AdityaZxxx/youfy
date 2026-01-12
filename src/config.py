import json
import os
from rich.console import Console

# Use standard XDG config path
CONFIG_DIR = os.path.expanduser("~/.config/spotube")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
console = Console()

class ConfigManager:
    @staticmethod
    def _ensure_config_dir():
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR)

    @staticmethod
    def load_config():
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    @staticmethod
    def save_config(config_data):
        ConfigManager._ensure_config_dir()
        # Load existing config first to not overwrite other keys
        current_config = ConfigManager.load_config()
        current_config.update(config_data)
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(current_config, f, indent=4)
        
        console.print(f"[green]Configuration saved to {CONFIG_FILE}[/green]")

    @staticmethod
    def get_spotify_credentials():
        config = ConfigManager.load_config()
        return config.get('spotify_client_id'), config.get('spotify_client_secret')
