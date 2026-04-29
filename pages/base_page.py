"""
Base Page Object — shared utilities for all page objects.
"""

import logging
import os
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


class BasePage:
    """Provides common browser interactions with built-in explicit waits."""

    DEFAULT_TIMEOUT: int = 20

    _COOKIE_ACCEPT = (
        By.CSS_SELECTOR,
        "button#wt-cli-accept-all-btn, "
        "button[aria-label*='Accept'], "
        "button[data-testid*='accept'], "
        ".cookie-accept, #accept-cookies",
    )

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def open(self, url: str) -> None:
        logger.info("Navigating to: %s", url)
        self.driver.get(url)
        self.dismiss_cookie_banner()

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    # ------------------------------------------------------------------
    # Element retrieval
    # ------------------------------------------------------------------

    def find_element(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator),
            message=f"Element not found: {locator}",
        )

    def find_elements(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> list:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            return []
        return self.driver.find_elements(*locator)

    def find_visible_element(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator),
            message=f"Element not visible: {locator}",
        )

    def find_clickable_element(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> WebElement:
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator),
            message=f"Element not clickable: {locator}",
        )

    # ------------------------------------------------------------------
    # Interactions
    # ------------------------------------------------------------------

    def click(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> None:
        element = self.find_clickable_element(locator, timeout)
        logger.debug("Clicking element: %s", locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        try:
            element.click()
        except Exception:
            logger.warning("Standard click failed for %s, trying JS click", locator)
            self.driver.execute_script("arguments[0].click();", element)

    def js_click(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> None:
        """JavaScript click — fallback for elements that intercept pointer events."""
        element = self.find_element(locator, timeout)
        logger.debug("JS-clicking element: %s", locator)
        self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator: tuple, text: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        element = self.find_visible_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    def scroll_to(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> None:
        element = self.find_element(locator, timeout)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

    def dismiss_cookie_banner(self) -> None:
        """Attempt to dismiss the cookie consent banner with multiple common selectors."""
        selectors = [
            (By.CSS_SELECTOR, "button#wt-cli-accept-all-btn"),
            (By.ID, "wt-cli-accept-all-btn"),
            (By.XPATH, "//button[contains(text(), 'Accept All')]"),
            (By.XPATH, "//a[contains(text(), 'Accept All')]")
        ]
        for selector in selectors:
            try:
                # Use a short timeout for each selector to avoid hanging
                element = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable(selector)
                )
                logger.info("Dismissing cookie consent banner via %s", selector)
                self.driver.execute_script("arguments[0].click();", element)
                time.sleep(1) # Wait for animation
                return
            except Exception:
                continue

    # ------------------------------------------------------------------
    # Waits & visibility checks
    # ------------------------------------------------------------------

    def wait_for_url_contains(self, fragment: str, timeout: int = DEFAULT_TIMEOUT) -> bool:
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.url_contains(fragment),
                message=f"URL did not contain '{fragment}' within {timeout}s",
            )
        except TimeoutException:
            logger.error("URL check failed. Current URL: %s", self.get_current_url())
            return False

    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element_to_disappear(self, locator: tuple, timeout: int = DEFAULT_TIMEOUT) -> None:
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator),
            message=f"Element did not disappear: {locator}",
        )

    # ------------------------------------------------------------------
    # Window / tab management
    # ------------------------------------------------------------------

    def switch_to_new_tab(self, original_handle: str, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Switch to any newly opened tab/window."""
        WebDriverWait(self.driver, timeout).until(
            lambda d: len(d.window_handles) > 1,
            message="New tab did not open within timeout",
        )
        for handle in self.driver.window_handles:
            if handle != original_handle:
                self.driver.switch_to.window(handle)
                logger.info("Switched to new tab: %s", handle)
                return

    def close_current_tab_and_switch_back(self, original_handle: str) -> None:
        self.driver.close()
        self.driver.switch_to.window(original_handle)

    # ------------------------------------------------------------------
    # Screenshot
    # ------------------------------------------------------------------

    def take_screenshot(self, name: str = "screenshot") -> str:
        reports_dir = os.path.join(os.path.dirname(__file__), "..", "reports")
        os.makedirs(reports_dir, exist_ok=True)
        path = os.path.join(reports_dir, f"{name}.png")
        self.driver.save_screenshot(path)
        logger.info("Screenshot saved: %s", path)
        return path
