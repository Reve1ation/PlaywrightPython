
class EbaySearchResultsPageLocators:
    FILTER_BASE = '//li[@class and .//h3[text() = "{}"]]//span[text() = "{}"]'
    SEARCH_RESULTS = '//div[@id="srp-river-results"]//li[@id]//span[@role="heading"]/ancestor::a'
    FILTER_SELECT = '//ul[@class="fake-tabs__items"]//span[text()="{}"]'
    # BUY_IT_NOW_FILTER = '//ul[@class="fake-tabs__items"]//span[text()="Buy It Now"]'
    # AUCTION_FILTER = '//ul[@class="fake-tabs__items"]//span[text()="Auction"]'