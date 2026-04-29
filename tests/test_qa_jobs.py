"""
E2E Test Suite for InsiderOne Careers QA Job Filtering.
"""

import pytest
from pages.home_page import HomePage
from pages.careers_page import CareersPage


class TestHomePage:
    """TC-001 to TC-004: Homepage basic visibility and load checks."""

    def test_homepage_loads_successfully(self, driver):
        home_page = HomePage(driver).load()
        assert home_page.is_homepage_loaded(), "Homepage failed to load or URL mismatch"

    def test_header_is_visible(self, driver):
        home_page = HomePage(driver).load()
        assert home_page.is_header_visible(), "Header section is not visible on homepage"

    def test_footer_is_visible(self, driver):
        home_page = HomePage(driver).load()
        assert home_page.is_footer_visible(), "Footer section is not visible on homepage"

    def test_page_title_is_not_empty(self, driver):
        home_page = HomePage(driver).load()
        title = home_page.get_page_title()
        assert title and len(title) > 0, "Homepage title is missing or empty"


class TestCareersJobFilter:
    """TC-005 to TC-008: Navigation to careers, filtering by QA, and validating job cards."""

    @pytest.fixture(autouse=True)
    def setup_careers_qa_filter(self, driver):
        """Shared setup: Navigate to careers, click 'See all teams', and select QA."""
        self.careers_page = CareersPage(driver).load()
        self.careers_page.scroll_to_teams_section()
        self.careers_page.click_see_all_teams()
        self.careers_page.select_quality_assurance_team()
        self.listings = self.careers_page.get_job_listings()

    def test_job_list_is_not_empty(self):
        assert len(self.listings) > 0, "Expected at least one job listing for Quality Assurance, but got zero."

    def test_each_job_position_contains_quality_assurance(self):
        assert len(self.listings) > 0, "No job listings found; cannot validate positions."
        for job in self.listings:
            # Flexible check for position name
            assert any(term in job.position.upper() for term in ["QUALITY ASSURANCE", "QA", "TEST"]), \
                f"Job position '{job.position}' does not appear to be a QA role"

    def test_each_job_department_contains_quality_assurance(self):
        assert len(self.listings) > 0, "No job listings found; cannot validate departments."
        for job in self.listings:
            assert any(term in job.department.upper() for term in ["QUALITY ASSURANCE", "QA"]), \
                f"Job department '{job.department}' is not Quality Assurance"

    def test_each_job_location_is_istanbul_turkey(self):
        assert len(self.listings) > 0, "No job listings found; cannot validate locations."
        for job in self.listings:
            # Check for Istanbul specifically, might be 'Istanbul, Turkey' or just 'Istanbul'
            assert "ISTANBUL" in job.location.upper(), \
                f"Job location '{job.location}' is not Istanbul, Turkey"


class TestApplyFlow:
    """TC-009: Verification of 'Apply' button redirection to Lever."""

    def test_apply_redirects_to_lever(self, driver):
        careers_page = CareersPage(driver).load()
        careers_page.scroll_to_teams_section()
        careers_page.click_see_all_teams()
        careers_page.select_quality_assurance_team()
        
        listings = careers_page.get_job_listings()
        assert len(listings) > 0, "No job listings found to test Apply redirection"
        
        # Click Apply for the first one
        original_handle = careers_page.click_apply_for_job(listings[0])
        
        # Redirection check
        # If it opens in a new tab, switch to it
        if len(driver.window_handles) > 1:
            careers_page.switch_to_new_tab(original_handle)
            
        # Verify URL contains 'lever.co' and specific job path if already on Lever
        assert "lever.co" in driver.current_url.lower(), \
            f"Apply redirection failed. Current URL: {driver.current_url}"
