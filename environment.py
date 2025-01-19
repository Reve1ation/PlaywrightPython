from utilities.common import load_configurations, initialize_browsers
from playwright.sync_api import sync_playwright
from utilities.logger import LOGGER

def before_all(context):
    LOGGER.info("Starting Playwright configuration.")

    # Завантаження конфігурацій
    context.configurations = load_configurations()

    # Запуск Playwright
    context.playwright = sync_playwright().start()

    # Ініціалізація браузерів
    context.browsers = initialize_browsers(context.playwright, context.configurations)

    LOGGER.info("Playwright configuration completed.")

def before_scenario(context, scenario):
    LOGGER.info(f"Starting scenario: {scenario.name}")

    if not hasattr(context, "current_configuration_index"):
        context.current_configuration_index = 0

    config = context.configurations[context.current_configuration_index]
    context.browser = context.browsers[config["browser"]]
    context.device = config["device"]

    LOGGER.debug(f"Selected configuration: {config}")

    context.current_configuration_index = (context.current_configuration_index + 1) % len(context.configurations)

    try:
        if context.device:
            context.context = context.browser.new_context(**context.playwright.devices[context.device])
            LOGGER.info(f"Using device: {context.device}")
        else:
            context.context = context.browser.new_context()
            LOGGER.info("Using default desktop configuration.")

        context.page = context.context.new_page()
    except Exception as e:
        LOGGER.critical(f"Failed to initialize context or page: {e}")
        raise

def after_scenario(context, scenario):
    LOGGER.info(f"Ending scenario: {scenario.name}")

    try:
        context.page.close()
        context.context.close()
    except Exception as e:
        LOGGER.error(f"Error while releasing resources: {e}")

def after_all(context):
    LOGGER.info("Shutting down Playwright.")

    try:
        for browser in context.browsers.values():
            browser.close()

        context.playwright.stop()
    except Exception as e:
        LOGGER.error(f"Error during shutdown: {e}")
