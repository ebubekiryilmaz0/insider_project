"""
conftest.py — pytest fixtures shared across the entire test suite.

Driver lifecycle:
    - `driver` fixture: function-scoped (one browser per test)
    - Headless mode controlled by --headless CLI flag (default: True)
    - Browser type controlled by --browser CLI flag (default: chrome)

Reporting:
    - Screenshots captured automatically on test failure
    - Stored in reports/screenshots/
"""

import logging
import os

import pytest

from utils.driver_factory import create_driver

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# ---------------------------------------------------------------------------
# Custom CLI options
# ---------------------------------------------------------------------------

def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use: chrome (default) | firefox",
    )
    parser.addoption(
        "--headless",
        action="store",
        default="true",
        help="Run in headless mode: true (default) | false",
    )


# ---------------------------------------------------------------------------
# Driver fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest):
    """
    Provides a WebDriver instance for each test function.
    Automatically quits the driver and captures a screenshot on failure.
    """
    browser = request.config.getoption("--browser")
    headless_str = request.config.getoption("--headless")
    headless = headless_str.lower() not in ("false", "0", "no")

    web_driver = create_driver(browser=browser, headless=headless)
    logger.info("Driver started for test: %s", request.node.name)

    yield web_driver

    # -----------------------------------------------------------------------
    # Teardown — screenshot on failure, then quit
    # -----------------------------------------------------------------------
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        _capture_failure_screenshot(web_driver, request.node.name)

    web_driver.quit()
    logger.info("Driver closed for test: %s", request.node.name)


# ---------------------------------------------------------------------------
# Hook: attach screenshot to pytest-html report on failure
# ---------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call):
    outcome = yield
    report = outcome.get_result()

    # Attach phase result to the item so the driver fixture can read it
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver is not None:
            screenshot_path = _capture_failure_screenshot(driver, item.name)
            if screenshot_path:
                _attach_screenshot_to_report(item, screenshot_path)


def _capture_failure_screenshot(driver, test_name: str) -> str | None:
    """Save a PNG screenshot and return its absolute path."""
    screenshots_dir = os.path.join(
        os.path.dirname(__file__), "reports", "screenshots"
    )
    os.makedirs(screenshots_dir, exist_ok=True)

    safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in test_name)
    path = os.path.join(screenshots_dir, f"{safe_name}.png")
    try:
        driver.save_screenshot(path)
        logger.info("Failure screenshot saved: %s", path)
        return path
    except Exception as exc:
        logger.warning("Could not save screenshot: %s", exc)
        return None


def _attach_screenshot_to_report(item: pytest.Item, screenshot_path: str) -> None:
    """Embed the screenshot in the pytest-html report."""
    try:
        from pytest_html import extras  # type: ignore

        extra_list = getattr(item, "extras", [])
        extra_list.append(extras.image(screenshot_path))
        item.extras = extra_list
    except Exception:
        pass  # pytest-html not installed or API changed — non-fatal
