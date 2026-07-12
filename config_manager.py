import os
import json

class ConfigManager:
    def __init__(self):
        appdata = os.getenv('APPDATA')
        if not appdata:
            appdata = os.path.expanduser('~') # fallback
        self.app_dir = os.path.join(appdata, 'LightMonitor')
        self.config_path = os.path.join(self.app_dir, 'config.json')
        
        self.default_config = {
            "overlay": {
                "transparency": 0.85,
                "position": {"x": 100, "y": 100},
                "click_through": False,
                "enabled_metrics": ["cpu_usage", "gpu_usage", "vram_usage", "ram_usage"],
                "metric_order": ["cpu_usage", "gpu_usage", "vram_usage", "ram_usage"]
            }
        }
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            return self.default_config
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except:
            return self.default_config

    def save_config(self):
        os.makedirs(self.app_dir, exist_ok=True)
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"[Config] Error saving config: {e}")
            
    def get_overlay_conf(self):
        if "overlay" not in self.config:
            self.config["overlay"] = self.default_config["overlay"]
        # Handle case where fields might be missing in existing config
        for key, val in self.default_config["overlay"].items():
            if key not in self.config["overlay"]:
                self.config["overlay"][key] = val
        return self.config["overlay"]
