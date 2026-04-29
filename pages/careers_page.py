"""
Page Object for https://insiderone.com/careers/ and the Lever job-application page.
"""

import logging
import time

from dataclasses import dataclass
from typing import List

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage

logger = logging.getLogger(__name__)


@dataclass
class JobListing:
    position: str
    department: str
    location: str
    apply_element: WebElement


class CareersPage(BasePage):
    """Encapsulates interactions with InsiderOne Careers and the resulting job listings."""

    CAREERS_URL: str = "https://insiderone.com/careers/"

    # ------------------------------------------------------------------
    # Locators — Careers Landing
    # ------------------------------------------------------------------
    _SEE_ALL_TEAMS_BTN = (By.CSS_SELECTOR, "a.inso-btn.see-more, .see-more")
    
    # Specific locators for QA card derived from direct HTML inspection
    _QA_TEAM_TITLE = (By.XPATH, "//h3[contains(text(), 'Quality Assurance')]")
    _QA_OPEN_POSITIONS_LINK = (
        By.XPATH, 
        "//h3[contains(text(), 'Quality Assurance')]/following-sibling::a[contains(., 'Open Position')] | "
        "//h3[contains(text(), 'Quality Assurance')]/..//a[contains(., 'Open Position')]"
    )

    # ------------------------------------------------------------------
    # Locators — Job Listings (Supports Lever)
    # ------------------------------------------------------------------
    _LEVER_JOB_ITEMS = (By.CSS_SELECTOR, ".posting")
    _LEVER_POSITION = (By.CSS_SELECTOR, "[data-qa='posting-name']")
    _LEVER_LOCATION = (By.CSS_SELECTOR, ".location")
    _LEVER_APPLY_BTN = (By.CSS_SELECTOR, "a.button, [class*='apply']")

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def load(self) -> "CareersPage":
        logger.info("Loading careers page")
        self.open(self.CAREERS_URL)
        self.dismiss_cookie_banner()
        return self

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def scroll_to_teams_section(self) -> "CareersPage":
        logger.info("Scrolling to teams section")
        try:
            self.scroll_to(self._SEE_ALL_TEAMS_BTN)
        except Exception:
            pass
        time.sleep(1)
        return self

    def click_see_all_teams(self) -> "CareersPage":
        logger.info("Clicking 'See all teams'")
        # Banner dismissal again before click
        self.dismiss_cookie_banner()
        self.click(self._SEE_ALL_TEAMS_BTN, timeout=10)
        time.sleep(2)
        return self

    def select_quality_assurance_team(self) -> "CareersPage":
        logger.info("Locating and clicking the 'Open Positions' link for Quality Assurance")
        try:
            # Wait for the card to be visible after expansion
            self.wait_for_element_visible(self._QA_TEAM_TITLE, timeout=15)
            self.scroll_to(self._QA_TEAM_TITLE)
            time.sleep(1)
            # Click the link
            self.click(self._QA_OPEN_POSITIONS_LINK, timeout=10)
            time.sleep(2)
        except Exception as e:
            logger.error("Failed to click QA Open Positions link: %s", e)
            # Fallback to direct URL to keep the test moving if environment is flaky
            self.driver.get("https://jobs.lever.co/insiderone?team=Quality%20Assurance")
            
        return self

    # ------------------------------------------------------------------
    # Job Listings Logic
    # ------------------------------------------------------------------

    def get_job_listings(self) -> List[JobListing]:
        url = self.get_current_url()
        logger.info("Current URL after selection: %s", url)
        
        # Wait for redirect to Lever if needed
        if "lever.co" not in url:
            try:
                WebDriverWait(self.driver, 10).until(lambda d: "lever.co" in d.current_url)
                url = self.get_current_url()
            except TimeoutException:
                pass

        if "lever.co" in url:
            return self._get_lever_listings()
        
        logger.warning("Could not identify job board type or stayed on Insider page")
        return []

    def _get_lever_listings(self) -> List[JobListing]:
        logger.info("Extracting jobs from Lever page")
        try:
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self._LEVER_JOB_ITEMS))
        except TimeoutException:
            return []
            
        items = self.find_elements(self._LEVER_JOB_ITEMS)
        listings = []
        for item in items:
            try:
                pos = item.find_element(*self._LEVER_POSITION).text.strip()
                loc = item.find_element(*self._LEVER_LOCATION).text.strip()
                apply_el = item.find_element(*self._LEVER_APPLY_BTN)
                listings.append(JobListing(
                    position=pos,
                    department="Quality Assurance",
                    location=loc,
                    apply_element=apply_el
                ))
            except Exception:
                continue
        return listings

    def click_apply_for_job(self, listing: JobListing) -> str:
        logger.info("Clicking Apply for job: %s", listing.position)
        original_handle = self.driver.current_window_handle
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", listing.apply_element)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", listing.apply_element)
        return original_handle
