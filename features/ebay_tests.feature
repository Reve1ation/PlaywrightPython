
Feature: eBay.com Functionality
  # Playwright practise

  @id_1
  Scenario: User can search for a product
    Given the user opens eBay main page
    Then the eBay main page is displayed
    When the user searches "iPhone"
    Then the eBay search results page has specific results

