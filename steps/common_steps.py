from behave import given, when, then
from pages.ebay_main_page import EbayMainPage
from pages.ebay_search_resulats_page import EbaySearchResultsPage


@given("the user opens eBay main page")
def step_given_user_opens_main_page(context):
    context.ebay_main_page = EbayMainPage(context.page, context.ui_config)
    context.ebay_main_page.load()


@then("the eBay main page is displayed")
def step_then_main_page_is_displayed(context):
    assert context.ebay_main_page.verify_elements_present(), "Main page elements are not displayed."


@when('the user searches "{query}"')
def step_when_user_searches(context, query):
    context.ebay_main_page.perform_search_of_item(query)


@then("the eBay search results page has specific results")
def step_then_search_results_page_has_results(context):
    search_results_page = EbaySearchResultsPage(context.page, context.ui_config)
    assert search_results_page.results_contains_text("iPhone"), "Search results do not match the search term."
