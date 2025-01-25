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
    """
        Loads the configuration settings for the Playwright framework.

        - Reads YAML configuration from the `config/ebay_prod.yaml` file.
        - Loads environment variables for dynamic settings such as browsers and devices.
        - Configures the logging level dynamically based on the `LOG_LEVEL` environment variable.
        Returns:
            tuple: A tuple containing:
                - configurations (list): List of browser and device configurations.
                - yaml_config (dict): Loaded YAML configuration data.
        Raises:
            FileNotFoundError: If the YAML configuration file is not found.
    """
    LOGGER.configure_logger(level=os.getenv("LOG_LEVEL", "INFO").upper())
    LOGGER.info("Loading configurations.")

    if not load_dotenv():
        LOGGER.critical(".env file not found or not loaded.")

    # Load YAML configuration
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / "config" / "ebay_prod.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    with config_path.open("r") as config_file:
        yaml_config = yaml.safe_load(config_file)

    LOGGER.debug(f"YAML Configuration: {yaml_config}")

    # Load environment variables for dynamic configurations
    browsers = os.getenv("BROWSERS", "chromium").split(",")
    devices = os.getenv("DEVICES", "").split(",")
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
    """
        Initializes the browsers specified in the configurations.

        This function takes a Playwright instance and a list of configurations,
        then launches the specified browsers (chromium, firefox, or webkit)
        in either headless or non-headless mode.

        Args:
            playwright: The Playwright instance used to control browsers.
            configurations (list): A list of dictionaries, each containing:
                - "browser" (str): The name of the browser to initialize ("chromium", "firefox", or "webkit").
                - "device" (str, optional): The device configuration (if applicable).
                - "headless" (bool): Whether to run the browser in headless mode.

        Returns:
            dict: A dictionary where the keys are browser names (str)
                  and the values are browser instances.

        Raises:
            Exception: If the browser fails to initialize, an error is logged, and the browser is skipped.

        Example:
            configurations = [
                {"browser": "chromium", "device": None, "headless": True},
                {"browser": "firefox", "device": "iPhone 15 Plus", "headless": False}
            ]
            browsers = initialize_browsers(playwright, configurations)
        """
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
