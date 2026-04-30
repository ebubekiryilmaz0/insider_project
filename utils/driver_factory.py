"""
WebDriver factory — creates and configures Chrome/Firefox instances.
Supports headless mode for CI environments (GitHub Actions, Docker, etc.).
"""

import logging
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

try:
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    WDM_AVAILABLE = True
except ImportError:
    WDM_AVAILABLE = False

logger = logging.getLogger(__name__)

# Supported browsers
CHROME = "chrome"
FIREFOX = "firefox"


def create_driver(
    browser: str = CHROME,
    headless: bool = True,
    window_size: tuple[int, int] = (1920, 1080),
) -> webdriver.Remote:
    """
    Factory function that returns a fully configured WebDriver instance.

    Args:
        browser:     'chrome' (default) or 'firefox'
        headless:    If True, runs without a GUI (CI-friendly)
        window_size: (width, height) tuple for the browser viewport

    Returns:
        A WebDriver instance ready for use.
    """
    browser = browser.lower()
    logger.info("Creating %s driver (headless=%s)", browser, headless)

    if browser == CHROME:
        return _create_chrome(headless, window_size)
    if browser == FIREFOX:
        return _create_firefox(headless, window_size)

    raise ValueError(f"Unsupported browser: '{browser}'. Use 'chrome' or 'firefox'.")


# ------------------------------------------------------------------
# Chrome
# ------------------------------------------------------------------

def _create_chrome(headless: bool, window_size: tuple[int, int]) -> webdriver.Chrome:
    options = ChromeOptions()

    if headless:
        options.add_argument("--headless=new")

    width, height = window_size
    options.add_argument(f"--window-size={width},{height}")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--remote-debugging-port=9222")

    # Suppress DevTools / USB noise in logs
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Use a realistic user-agent to avoid bot detection
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    if WDM_AVAILABLE:
        try:
            driver_path = ChromeDriverManager().install()
            # Fix for WDM bug where it sometimes returns a text file path instead of .exe
            if not driver_path.lower().endswith(".exe"):
                base_dir = os.path.dirname(driver_path)
                exe_path = os.path.join(base_dir, "chromedriver.exe")
                if os.path.exists(exe_path):
                    driver_path = exe_path
                else:
                    # Search recursively for chromedriver.exe in the base_dir
                    for root, dirs, files in os.walk(base_dir):
                        if "chromedriver.exe" in files:
                            driver_path = os.path.join(root, "chromedriver.exe")
                            break
            service = ChromeService(driver_path)
        except Exception as e:
            logger.warning("ChromeDriverManager failed (%s). Falling back to Selenium Manager.", e)
            service = ChromeService()
    else:
        service = ChromeService()  # assumes chromedriver is on PATH or handled by Selenium Manager

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(0)  # rely solely on explicit waits
    logger.info("Chrome driver created successfully")
    return driver


# ------------------------------------------------------------------
# Firefox
# ------------------------------------------------------------------

def _create_firefox(headless: bool, window_size: tuple[int, int]) -> webdriver.Firefox:
    options = FirefoxOptions()

    if headless:
        options.add_argument("--headless")

    width, height = window_size
    options.add_argument(f"--width={width}")
    options.add_argument(f"--height={height}")

    if WDM_AVAILABLE:
        try:
            service = FirefoxService(GeckoDriverManager().install())
        except Exception as e:
            logger.warning("GeckoDriverManager failed (%s). Falling back to Selenium Manager.", e)
            service = FirefoxService()
    else:
        service = FirefoxService()

    driver = webdriver.Firefox(service=service, options=options)
    driver.set_page_load_timeout(60)
    driver.implicitly_wait(0)
    logger.info("Firefox driver created successfully")
    return driver
