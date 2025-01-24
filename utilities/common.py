import os
import yaml
from dotenv import load_dotenv
from pathlib import Path
from itertools import product
from utilities.logger import LOGGER

# Load environment variables
load_dotenv()

# Load configurations from YAML file
def load_configurations():
    LOGGER.info("Loading configurations.")

    # Load YAML configuration
    base_dir = Path(__file__).resolve().parent.parent
    config_path = base_dir / "config" / "ebay_prod.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    with config_path.open("r") as config_file:
        yaml_config = yaml.safe_load(config_file)

    LOGGER.debug(f"YAML Configuration: {yaml_config}")

    # Load environment variables for dynamic configurations
    browsers = os.getenv("BROWSERS", "chromium").split(",")
    devices = os.getenv("DEVICE", "").split(",")
    headless = os.getenv("HEADLESS", "true").lower() == "true"

    LOGGER.debug(f"Environment browsers: {browsers}")
    LOGGER.debug(f"Environment devices: {devices}")
    LOGGER.debug(f"Headless mode: {headless}")

    configurations = []
    for browser_name, device_name in product(browsers, devices):
        configurations.append({
            "browser": browser_name.strip(),
            "device": device_name.strip() if device_name.strip() else None,
            "headless": headless,
        })

    LOGGER.debug(f"Generated configurations: {configurations}")
    return configurations, yaml_config

def initialize_browsers(playwright, configurations):
    LOGGER.info("Initializing browsers.")
    browsers = {}

    for config in configurations:
        browser_name = config["browser"]
        if browser_name not in browsers:
            try:
                if browser_name == "firefox":
                    browsers[browser_name] = playwright.firefox.launch(headless=config["headless"])
                elif browser_name == "webkit":
                    browsers[browser_name] = playwright.webkit.launch(headless=config["headless"])
                else:
                    browsers[browser_name] = playwright.chromium.launch(headless=config["headless"])

                LOGGER.info(f"Browser '{browser_name}' initialized successfully.")
            except Exception as e:
                LOGGER.error(f"Failed to initialize browser '{browser_name}': {e}")

    return browsers
