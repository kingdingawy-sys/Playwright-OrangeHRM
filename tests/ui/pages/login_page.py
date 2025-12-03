"""
Login Page Object
"""
from playwright.sync_api import Page, expect
from tests.ui.pages.base_page import BasePage
from utilities.logger import get_logger
from config.settings import URLs

logger = get_logger(__name__)


class LoginPage(BasePage):
    """Login Page interactions"""

    def __init__(self, page: Page):
        super().__init__(page)

        # Locators
        self.username_input = "input[name='username']"
        self.password_input = "input[name='password']"
        self.login_button = "button[type='submit']"
        self.error_message = ".oxd-alert-content-text"
        self.forgot_password_link = "text=Forgot your password?"
        self.logo = ".orangehrm-login-branding img"
        self.login_container = ".orangehrm-login-container"

    def navigate(self):
        """Navigate to login page"""
        logger.info("Navigating to Login page")
        self.navigate_to(URLs.LOGIN)

    def enter_username(self, username: str):
        """Enter username"""
        logger.info(f"Entering username: {username}")
        self.fill(self.username_input, username)

    def enter_password(self, password: str):
        """Enter password"""
        logger.info("Entering password")
        self.fill(self.password_input, password)

    def click_login_button(self):
        """Click login button"""
        logger.info("Clicking login button")
        self.click(self.login_button)
        self.wait_for_loading_to_disappear()

    def login(self, username: str, password: str):
        """
        Complete login flow

        Args:
            username: Username
            password: Password
        """
        logger.info(f"Logging in with username: {username}")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

    def is_error_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self.is_visible(self.error_message, timeout=3000)

    def get_error_message(self) -> str:
        """Get error message text"""
        if self.is_error_displayed():
            return self.get_text(self.error_message)
        return ""

    def click_forgot_password(self):
        """Click forgot password link"""
        logger.info("Clicking forgot password link")
        self.click(self.forgot_password_link)

    def is_login_page_loaded(self) -> bool:
        """Check if login page is loaded"""
        return self.is_visible(self.login_container)

    def is_logo_visible(self) -> bool:
        """Check if logo is visible"""
        return self.is_visible(self.logo)

    # Assertions
    def assert_on_login_page(self):
        """Assert user is on login page"""
        self.assert_element_visible(self.login_container, "Login page should be visible")
        self.assert_url_contains("/auth/login")
        logger.info("✅ On login page")

    def assert_login_successful(self):
        """Assert login was successful"""
        self.wait_for_url("**/dashboard/index", timeout=10000)
        # Now handle the dashboard modal before asserting
        from tests.ui.pages.dashboard_page import DashboardPage
        dashboard = DashboardPage(self.page)
        dashboard.handle_first_login_modal()
        self.assert_url_contains("/dashboard")
        logger.info("✅ Login successful")

    def assert_error_message_displayed(self, expected_message: str = None):
        """Assert error message is displayed"""
        self.assert_element_visible(self.error_message, "Error message should be displayed")
        if expected_message:
            actual_message = self.get_error_message()
            assert expected_message in actual_message, \
                f"Expected '{expected_message}' in error message, got: {actual_message}"
        logger.info("✅ Error message displayed")