from config.settings import BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD
from tests.mobile.pages.mobile_login_page import MobileLoginPage
from tests.mobile.pages.mobile_dashboard_page import MobileDashboardPage


def test_mobile_dashboard_elements_visible(mobile_page):

    # Arrange: Navigate and log in
    mobile_page.goto(BASE_URL)
    login_page = MobileLoginPage(mobile_page)
    login_page.login(ADMIN_USERNAME, ADMIN_PASSWORD)
    mobile_page.wait_for_url("**/dashboard/index", timeout=10000)

    # Act & Assert: Check essential dashboard elements
    dashboard = MobileDashboardPage(mobile_page)

    # 1. Dashboard header must be visible
    assert dashboard.dashboard_header.is_visible(), "Dashboard header is not visible"

    # 2. Quick Launch widget (common on OrangeHRM dashboard) should appear
    assert dashboard.quick_launch_widget.is_visible(), "Quick Launch widget not found on dashboard"

    # Optional: You can add more stable elements like "My Actions" or "Assign Leave"
    # my_actions = mobile_page.get_by_text("My Actions")
    # assert my_actions.is_visible()