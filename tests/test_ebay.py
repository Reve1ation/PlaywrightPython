import pytest

from pages.ebay_main_page import EbayMainPage
from pages.ebay_search_resulats_page import EbaySearchResultsPage

@pytest.mark.smoke
def test_search_functionality(page, ui_config):
    ebay_main_page = EbayMainPage(page, ui_config)
    ebay_main_page.load()

    assert ebay_main_page.verify_elements_present(), "Main page elements are not displayed."

    search_term = "iPhone"
    ebay_main_page.perform_search_of_item(search_term)

    search_results_page = EbaySearchResultsPage(page, ui_config)
    assert search_results_page.results_contains_text(search_term), "Search results do not match the search term."


@pytest.mark.regression
def test_page_open(page, ui_config):
    ebay_main_page = EbayMainPage(page, ui_config)
    ebay_main_page.load()