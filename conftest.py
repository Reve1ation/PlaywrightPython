import pytest
from utilities.common import load_configurations, initialize_browsers
from playwright.sync_api import sync_playwright
from utilities.logger import LOGGER

@pytest.fixture(scope="session")
def configurations():
    configurations, _ = load_configurations()
    return configurations

@pytest.fixture(scope="session")
def ui_config():
    _, yaml_config = load_configurations()
    return yaml_config

@pytest.fixture(scope="session")
def playwright_instance():
    LOGGER.info("Starting Playwright instance.")
    playwright = sync_playwright().start()
    yield playwright
    playwright.stop()
    LOGGER.info("Playwright instance stopped.")

@pytest.fixture(scope="session")
def browsers(playwright_instance, configurations):
    return initialize_browsers(playwright_instance, configurations)

@pytest.fixture(scope="function")
def page(playwright_instance, browsers, configurations, request):
    config_index = getattr(request, "param", 0) % len(configurations)
    config = configurations[config_index]
    browser = browsers[config["browser"]]

    try:
        if config["device"]:
            context = browser.new_context(**playwright_instance.devices[config["device"]])
        else:
            context = browser.new_context()

        page = context.new_page()
        yield page

        page.close()
        context.close()
    except Exception as e:
        LOGGER.critical(f"Error during page setup or teardown: {e}")
        raise
