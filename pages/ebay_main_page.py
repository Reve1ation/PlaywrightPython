from pages.locators.ebay_main_page_locators import EbayMainPageLocators
from playwright.sync_api import Page as PlaywrightPage, Locator

from pages.locators.generic_ebay_page import GenericEbayPage
from utilities.logger import LOGGER


class EbayMainPage(GenericEbayPage):

    def __init__(self, page: PlaywrightPage, config: dict):
        super().__init__(page)
        self.page = page
        self.config = config
        self.URL = config['eBay']['base_url']

    def search_input(self) -> Locator:
        LOGGER.info("Accessing the search input field.")
        return self.find_element(EbayMainPageLocators.SEARCH_INPUT)

    def search_button(self) -> Locator:
        LOGGER.info("Accessing the search button.")
        return self.find_element(EbayMainPageLocators.SEARCH_BUTTON)

    def load(self):
        """
        Navigates to the eBay main page.

        Returns:
            EbayMainPage: The instance of the page class.
        """
        LOGGER.info(f"Opening URL: {self.URL}")
        self.page.goto(self.URL)
        LOGGER.info("eBay main page opened successfully.")
        return self

    def perform_search_of_item(self, query: str):
        """
            Performs a search operation on eBay.
            Args:
                query (str): The search term to input.
            Returns:
                EbayMainPage: The instance of the page class.
        """
        LOGGER.info(f"Performing search with query: {query}")
        search_input = self.search_input()
        search_input.focus()
        search_input.type(query)
        LOGGER.info("Search input filled successfully.")
        self.search_button().click()
        LOGGER.info("Search button clicked.")
        return self

    def verify_elements_present(self) -> bool:
        elements_to_verify = [self.search_input(), self.search_button()]

        for element in elements_to_verify:
            assert element.is_visible(), f"Element '{element}' is not visible."
        return True

