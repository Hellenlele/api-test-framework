import yaml
import os
from typing import Dict, Any


class ConfigManager:
    def __init__(self, config_file: str = None):
        if config_file is None:
            config_file = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        try:
            with open(self.config_file, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {self.config_file}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file: {e}")
    
    def get_environment_config(self, env_name: str = None) -> Dict[str, Any]:
        if env_name is None:
            env_name = os.getenv('TEST_ENV', 'demo')
        
        if env_name in self.config.get('environments', {}):
            return self.config['environments'][env_name]
        elif env_name in self.config:
            return self.config[env_name]
        else:
            available_envs = list(self.config.get('environments', {}).keys())
            raise ValueError(f"Environment '{env_name}' not found. Available: {available_envs}")
    
    def get_default_headers(self) -> Dict[str, str]:
        return self.config.get('default_headers', {})
    
    def get_test_settings(self) -> Dict[str, Any]:
        return self.config.get('test_settings', {})