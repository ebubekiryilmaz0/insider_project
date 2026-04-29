"""
Page Object for https://insiderone.com/ (Homepage).
"""

import logging

from selenium.webdriver.common.by import By

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """Encapsulates interactions and assertions for the InsiderOne homepage."""

    URL: str = "https://insiderone.com/"

    # ------------------------------------------------------------------
    # Locators
    # ------------------------------------------------------------------
    _HEADER = (By.CSS_SELECTOR, "header, #header, nav, [role='banner']")
    _FOOTER = (By.CSS_SELECTOR, "footer, #footer, [role='contentinfo']")
    _LOGO = (By.CSS_SELECTOR, "a[href='/'] img, .logo, header img")

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def load(self) -> "HomePage":
        self.open(self.URL)
        return self

    # ------------------------------------------------------------------
    # Assertions / queries
    # ------------------------------------------------------------------

    def is_homepage_loaded(self) -> bool:
        """Returns True if current URL matches the homepage origin."""
        current = self.get_current_url().rstrip("/")
        expected = self.URL.rstrip("/")
        return current == expected or current.startswith(expected)

    def is_header_visible(self) -> bool:
        return self.is_element_visible(self._HEADER)

    def is_footer_visible(self) -> bool:
        self.scroll_to(self._FOOTER)
        return self.is_element_visible(self._FOOTER)

    def get_page_title(self) -> str:
        return self.get_title()
