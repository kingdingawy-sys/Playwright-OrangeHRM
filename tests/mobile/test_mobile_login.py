import pytest
from config.settings import BASE_URL, ADMIN_USERNAME, ADMIN_PASSWORD
from tests.mobile.pages.mobile_login_page import MobileLoginPage


def test_mobile_login_success(mobile_page):

    # Arrange
    mobile_page.goto(BASE_URL)
    login_page = MobileLoginPage(mobile_page)

    # Act
    login_page.login(ADMIN_USERNAME, ADMIN_PASSWORD)

    # Assert
    # Wait for URL to change to dashboard
    mobile_page.wait_for_url("**/dashboard/index", timeout=10000)

    # Verify a key element on dashboard is visible (e.g., header containing "Dashboard")
    dashboard_header = mobile_page.get_by_role("heading", name="Dashboard")
    assert dashboard_header.is_visible(), "Dashboard header not visible after login"


def test_mobile_login_invalid_credentials(mobile_page):
    """Test login with invalid password on mobile"""
    mobile_page.goto(BASE_URL)
    login_page = MobileLoginPage(mobile_page)

    login_page.login(ADMIN_USERNAME, "wrong_password")

    # Verify error message appears
    error = login_page.error_message
    assert error.is_visible()
    assert "Invalid credentials" in error.text_content()