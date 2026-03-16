"""
Config Loader
Reads environment-specific settings from YAML files + .env overrides.
"""

import os
import yaml
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

_CONFIG_DIR = Path(__file__).parent.parent / "config"


def load_config(env: str = None) -> dict:
    """
    Load config for the given environment.
    Falls back to ENV environment variable, then 'dev'.
    """
    env = env or os.getenv("ENV", "dev")
    config_file = _CONFIG_DIR / f"{env}.yaml"

    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    with open(config_file) as f:
        config = yaml.safe_load(f)

    # Allow .env / shell env vars to override yaml values
    config["base_url"] = os.getenv("BASE_URL", config.get("base_url", ""))
    config["token"] = os.getenv("API_TOKEN", config.get("token", ""))
    config["api_key"] = os.getenv("API_KEY", config.get("api_key", ""))

    logger.info(f"Config loaded for environment: {env}")
    return config
