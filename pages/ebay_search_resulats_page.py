import random

from pages.locators.ebay_search_resulats_page_locators import EbaySearchResultsPageLocators
from pages.locators.generic_ebay_page import GenericEbayPage
from playwright.sync_api import Page as PlaywrightPage, Locator

from utilities.logger import LOGGER


class EbaySearchResultsPage(GenericEbayPage):

    def __init__(self, page: PlaywrightPage, config: dict):
        super().__init__(page)
        self.page = page
        self.config = config

    def search_results(self) -> Locator:
        LOGGER.info("Accessing search results elements.")
        return self.find_elements(EbaySearchResultsPageLocators.SEARCH_RESULTS)

    # def sell_type_filter_auction(self)-> Locator:
    #     LOGGER.info("Accessing the auction filter button.")
    #     return self.find_element(EbaySearchResultsPageLocators.AUCTION_FILTER)
    #
    # def sell_type_filter_buy_now(self)-> Locator:
    #     LOGGER.info("Accessing the buy now filter button.")
    #     return self.find_element(EbaySearchResultsPageLocators.BUY_IT_NOW_FILTER)

    def set_filter_by_name(self, fake_tab_name) -> Locator:
        LOGGER.info("Accessing the filter by name button.")
        return self.find_element(EbaySearchResultsPageLocators.FILTER_SELECT.format(fake_tab_name))

    def results_contains_text(self, search_text) -> bool:
        errors_counters = 0
        results = self.search_results()
        for index in range(results.count()):
            element = results.nth(index)
            if search_text.lower() not in element.inner_text().lower():
                LOGGER.warning(f"Element with mistake: {element.inner_text()}. Position = {index}")
                errors_counters += 1
        if errors_counters > 0:
            return False
        return True

    def open_random_item(self) ->"EbaySearchResultsPage":
        results: Locator = self.search_results()
        random_index = random.randint(0, results.count() - 1)
        element = results.nth(random_index)
        element.click()
        return self

    def set_ebay_filter(self, filter_name, filter_value) ->"EbaySearchResultsPage":
        filter_locator = EbaySearchResultsPageLocators.FILTER_BASE.format(filter_name, filter_value)
        self.find_element(filter_locator).click()
        return self

    def verify_elements_present(self):
        elements_to_verify = [self.search_results()]

        for element in elements_to_verify:
            assert element.is_visible(), f"Element '{element}' is not visible."
        return True