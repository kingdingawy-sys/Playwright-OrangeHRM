"""
Dashboard Page Object
"""
from playwright.sync_api import Page
from tests.ui.pages.base_page import BasePage
from utilities.logger import get_logger
from config.settings import URLs

logger = get_logger(__name__)


class DashboardPage(BasePage):
    """Dashboard Page interactions"""

    def __init__(self, page: Page):
        super().__init__(page)

        # Locators
        self.dashboard_title = "h6:has-text('Dashboard')"
        self.user_dropdown = ".oxd-userdropdown"
        self.logout_button = "text=Logout"

        # Menu items - using flexible approach
        self.admin_menu = ".oxd-main-menu-item:has-text('Admin')"
        self.pim_menu = ".oxd-main-menu-item:has-text('PIM')"
        self.leave_menu = ".oxd-main-menu-item:has-text('Leave')"
        self.time_menu = ".oxd-main-menu-item:has-text('Time')"
        self.recruitment_menu = ".oxd-main-menu-item:has-text('Recruitment')"
        self.my_info_menu = ".oxd-main-menu-item:has-text('My Info')"

        # Dashboard widgets
        self.time_at_work_widget = "text=Time at Work"
        self.quick_launch_widget = ".orangehrm-dashboard-widget"

        # First-time login modal
        self.first_login_modal = "div.modal--show h3:has-text('Welcome to OrangeHRM') OR div.modal--show h3:has-text('Welcome')"

    def handle_first_login_modal(self):
        """Handle the 'Welcome' modal that appears on first login"""
        try:
            if self.is_visible(self.first_login_modal, timeout=5000):
                logger.info("First login modal detected. Closing it.")
                # Close button is usually the 'x' in the top right
                close_button = self.page.locator("button:has-text('×'), button:has-text('Close')")
                if close_button.is_visible(timeout=2000):
                    close_button.click()
                    self.page.wait_for_timeout(1000)  # Give it time to disappear
                    logger.info("First login modal closed.")
        except Exception as e:
            logger.warning(f"No first login modal found or error handling it: {str(e)}")

    def is_dashboard_loaded(self) -> bool:
        """Check if dashboard is loaded"""
        return self.is_visible(self.dashboard_title)

    def get_dashboard_title(self) -> str:
        """Get dashboard title"""
        return self.get_text(self.dashboard_title)

    def click_user_dropdown(self):
        """Click user dropdown"""
        logger.info("Clicking user dropdown")
        self.click(self.user_dropdown)

    def logout(self):
        """Logout from application"""
        logger.info("Logging out")
        self.click_user_dropdown()
        self.page.wait_for_timeout(500)  # Small wait for dropdown
        self.click(self.logout_button)
        self.wait_for_url("**/auth/login")

    def navigate_to_admin(self):
        """Navigate to Admin page"""
        logger.info("Navigating to Admin")
        self.click(self.admin_menu)
        self.page.wait_for_timeout(1000)  # Wait for page transition
        self.wait_for_loading_to_disappear()

    def navigate_to_pim(self):
        """Navigate to PIM page"""
        logger.info("Navigating to PIM")
        self.click(self.pim_menu)
        self.page.wait_for_timeout(1000)
        self.wait_for_loading_to_disappear()

    def navigate_to_leave(self):
        """Navigate to Leave page"""
        logger.info("Navigating to Leave")
        self.click(self.leave_menu)
        self.page.wait_for_timeout(1000)
        self.wait_for_loading_to_disappear()

    def navigate_to_recruitment(self):
        """Navigate to Recruitment"""
        logger.info("Navigating to Recruitment")
        self.click(self.recruitment_menu)
        self.page.wait_for_timeout(1000)
        self.wait_for_loading_to_disappear()

    # Assertions
    def assert_on_dashboard(self):
        """Assert user is on dashboard"""
        # Handle first login modal if present
        self.handle_first_login_modal()
        self.assert_element_visible(self.dashboard_title, "Dashboard should be visible")
        self.assert_url_contains("/dashboard")
        logger.info("✅ On dashboard")