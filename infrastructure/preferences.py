import json
from pathlib import Path
from domain.interfaces import UserPreferences

class JsonUserPreferences(UserPreferences):
    def __init__(self, config_path: Path = Path.home() / ".subtitle_generator"):
        self.config_path = config_path
        self.config_file = self.config_path / "preferences.json"
        self.config_path.mkdir(parents=True, exist_ok=True)
        
        # Default preferences
        self.defaults = {
            "theme": "light",
            "default_language": "en",
            "output_directory": str(Path.home() / "Downloads"),
            "batch_size": 3,
            "notifications_enabled": True
        }

    def save_preferences(self, preferences: dict) -> None:
        with open(self.config_file, 'w') as f:
            json.dump(preferences, f, indent=4)

    def load_preferences(self) -> dict:
        try:
            with open(self.config_file, 'r') as f:
                return {**self.defaults, **json.load(f)}
        except FileNotFoundError:
            self.save_preferences(self.defaults)
            return self.defaults
