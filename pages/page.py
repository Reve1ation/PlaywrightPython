from typing import Literal
from playwright.sync_api import Page as PlaywrightPage, Locator
from utilities.logger import LOGGER

class Page:
    def __init__(self, page: PlaywrightPage):
        self.page = page

    def find_element(self,
                     selector: str,
                     state: Literal["attached", "detached", "hidden", "visible"] = "visible"
                     ) -> Locator:
        """
        Returns a locator for a single element with a specified state.

        Args:
            selector (str): The selector for the element.
            state (Literal["attached", "detached", "hidden", "visible"]): The state to wait for. Defaults to "visible".

        Returns:
            Locator: The locator for the element.
        """
        LOGGER.info(f"Finding element with selector: {selector}, state: {state}")
        locator = self.page.locator(selector)
        locator.wait_for(state=state)
        LOGGER.info(f"Element with selector '{selector}' found and ready.")
        return locator

    def find_elements(self,
                      selector: str,
                      state: Literal["attached", "detached", "hidden", "visible"] = "attached"
                      ) -> Locator:
        """
        Returns a locator for multiple elements with a specified state.

        Args:
            selector (str): The selector for the elements.
            state (Literal["attached", "detached", "hidden", "visible"]): The state to wait for. Defaults to "attached".

        Returns:
            Locator: The locator for the elements.
        """
        LOGGER.info(f"Finding elements with selector: {selector}, state: {state}")
        locator = self.page.locator(selector)
        locator.wait_for(state=state)
        count = locator.count()
        LOGGER.info(f"Elements with selector '{selector}' found and ready. Number of elements found: {count}")
        return locator

    def wait_for_element(self,
                         selector: str,
                         timeout: int = 30000,
                         state: Literal["attached", "detached", "hidden", "visible"] = "visible") -> None:
        """
        Waits for an element to reach a specified state within a timeout.

        Args:
            selector (str): The selector for the element.
            timeout (int): The maximum time to wait in milliseconds. Defaults to 30000.
            state (Literal["attached", "detached", "hidden", "visible"]): The state to wait for. Defaults to "visible".
        """
        LOGGER.info(f"Waiting for element with selector: {selector}, state: {state}, timeout: {timeout}ms")
        self.page.locator(selector).wait_for(state=state, timeout=timeout)
        LOGGER.info(f"Element with selector '{selector}' reached state '{state}'.")

    def wait_for_elements(self,
                          selector: str,
                          timeout: int = 5000,
                          state: Literal["attached", "detached", "hidden", "visible"] = "attached") -> Locator:
        """
        Waits for multiple elements to reach a specified state within a timeout.

        Args:
            selector (str): The selector for the elements.
            timeout (int): The maximum time to wait in milliseconds. Defaults to 5000.
            state (Literal["attached", "detached", "hidden", "visible"]): The state to wait for. Defaults to "attached".

        Returns:
            Locator: The locator for the elements.
        """
        self.page.wait_for_load_state("load")
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_load_state("networkidle")
        LOGGER.info(f"Waiting for elements with selector: {selector}, state: {state}, timeout: {timeout}ms")
        locator = self.page.locator(selector)
        locator.wait_for(state=state, timeout=timeout)
        count = locator.count()
        LOGGER.info(f"Elements with selector '{selector}' reached state '{state}'. Number of elements found: {count}")
        return locator
