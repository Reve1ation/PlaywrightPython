from typing import Literal

from playwright.sync_api import Locator

from pages.locators.generic_ebay_page_locators import GenericEbayPageLocators
from pages.page import Page
from utilities.logger import LOGGER


class GenericEbayPage(Page):
    def cart_button(self) -> Locator:
        LOGGER.info("Accessing the cart button.")
        return self.find_element(GenericEbayPageLocators.CART_BUTTON)

    def user_data_button(self) -> Locator:
        LOGGER.info("Accessing the user data button.")
        return self.find_element(GenericEbayPageLocators.SIGNED_IN_CONTROL)

    def guest_buttons(self) -> Locator:
        LOGGER.info("Accessing the guest buttons.")
        return self.find_element(GenericEbayPageLocators.GUEST_BUTTONS)

    def sign_out_button(self) -> Locator:
        LOGGER.info("Accessing the sign-out button.")
        return self.find_element(GenericEbayPageLocators.SIGN_OUT_BUTTON)

    def verify_signed_in(self, sign_in_status: Literal["signed in", "not signed in"]) -> bool:
        """
        Verifies the user's sign-in status.

        Args:
            sign_in_status (str): The expected sign-in status ("signed in" or "not signed in").

        Returns:
            bool: True if the sign-in status matches, otherwise False.

        Raises:
            ValueError: If the sign-in status is unexpected.
        """
        LOGGER.info(f"Verifying sign-in status: {sign_in_status}")
        match sign_in_status.lower():
            case 'signed in':
                return self.user_data_button().is_visible()
            case 'not signed in':
                return self.guest_buttons().is_visible()
            case _:
                raise ValueError(f"Unexpected sign-in status: '{sign_in_status}'")

    def sign_out(self) -> None:
        """
            Signs out the current user by clicking the appropriate buttons.
        """
        LOGGER.info("Signing out the user.")
        self.user_data_button().click()
        self.sign_out_button().click()
        assert self.verify_signed_in(sign_in_status="not signed in")
        LOGGER.info("User successfully signed out.")