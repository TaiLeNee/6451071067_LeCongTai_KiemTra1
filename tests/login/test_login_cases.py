from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import tempfile

from selenium import webdriver
from pages.login_page import LoginPage

import pytest

from tests.login.support import assert_authenticated, assert_rejected, require_env


def test_lg01_login_form_visible(login_page):
    visibility = login_page.form_visibility()

    for name, is_visible in visibility.items():
        assert is_visible, (
            f"Điều khiển '{name}' không hiển thị"
        )


def test_lg02_password_is_masked(login_page):
    password = "sample-password"
    login_page.fill_credentials("test_validation", password)

    assert login_page.password_type() == "password"
    assert login_page.password_value() == password


def test_lg03_valid_credentials_open_account(login_page):
    data = require_env(
        "UTC_TEST_USERNAME", "UTC_TEST_PASSWORD",
        "UTC_AUTH_IDENTITY_SELECTOR", "UTC_AUTH_IDENTITY_TEXT",
    )
    login_page.login(data["UTC_TEST_USERNAME"], data["UTC_TEST_PASSWORD"])
    assert_authenticated(login_page.driver)


def test_lg04_wrong_password_is_rejected(login_page):
    data = require_env(
        "UTC_TEST_USERNAME", "UTC_TEST_PASSWORD",
        "UTC_WRONG_PASSWORD", "UTC_INVALID_CREDENTIALS_TEXT",
    )
    assert data["UTC_WRONG_PASSWORD"] != data["UTC_TEST_PASSWORD"]
    login_page.login(data["UTC_TEST_USERNAME"], data["UTC_WRONG_PASSWORD"])
    assert_rejected(login_page, data["UTC_INVALID_CREDENTIALS_TEXT"])


def test_lg05_unknown_account_is_rejected(login_page):
    data = require_env(
        "UTC_UNKNOWN_USERNAME", "UTC_UNKNOWN_PASSWORD",
        "UTC_INVALID_CREDENTIALS_TEXT",
    )
    login_page.login(data["UTC_UNKNOWN_USERNAME"], data["UTC_UNKNOWN_PASSWORD"])
    assert_rejected(login_page, data["UTC_INVALID_CREDENTIALS_TEXT"])


def test_lg06_both_fields_empty(login_page):
    login_page.fill_credentials("", "")
    login_page.submit()
    assert_rejected(login_page, "Bạn chưa nhập tên đăng nhập")


def test_lg07_username_empty(login_page):
    login_page.fill_credentials("", "sample-password")
    login_page.submit()
    assert_rejected(login_page, "Bạn chưa nhập tên đăng nhập")


def test_lg08_password_empty(login_page):
    login_page.fill_credentials("test_validation", "")
    login_page.submit()
    assert_rejected(login_page, "Bạn chưa nhập mật khẩu")


def test_lg09_whitespace_username(login_page):
    login_page.fill_credentials("   ", "sample-password")
    login_page.submit()
    assert_rejected(login_page, "Tài khoản hoặc mật khẩu không đúng.")


def test_lg10_whitespace_password(login_page):
    data = require_env(
        "UTC_TEST_USERNAME", "UTC_TEST_PASSWORD",
        "UTC_INVALID_CREDENTIALS_TEXT",
    )
    assert data["UTC_TEST_PASSWORD"] != "   "
    login_page.login(data["UTC_TEST_USERNAME"], "   ")
    assert_rejected(login_page, data["UTC_INVALID_CREDENTIALS_TEXT"])


def test_lg11_enter_submits_valid_login(login_page):
    data = require_env(
        "UTC_TEST_USERNAME", "UTC_TEST_PASSWORD",
        "UTC_AUTH_IDENTITY_SELECTOR", "UTC_AUTH_IDENTITY_TEXT",
        "UTC_ENTER_SUPPORTED",
    )
    if data["UTC_ENTER_SUPPORTED"].lower() != "yes":
        pytest.skip("Not Applicable: Enter submission is not specified")
    login_page.fill_credentials(data["UTC_TEST_USERNAME"], data["UTC_TEST_PASSWORD"])
    login_page.submit_with_enter()
    assert_authenticated(login_page.driver)


def test_lg12_retry_after_wrong_password(login_page):
    data = require_env(
        "UTC_TEST_USERNAME", "UTC_TEST_PASSWORD",
        "UTC_WRONG_PASSWORD", "UTC_INVALID_CREDENTIALS_TEXT",
        "UTC_AUTH_IDENTITY_SELECTOR", "UTC_AUTH_IDENTITY_TEXT",
    )
    assert data["UTC_WRONG_PASSWORD"] != data["UTC_TEST_PASSWORD"]
    login_page.login(data["UTC_TEST_USERNAME"], data["UTC_WRONG_PASSWORD"])
    assert_rejected(login_page, data["UTC_INVALID_CREDENTIALS_TEXT"])
    login_page.fill_credentials(data["UTC_TEST_USERNAME"], data["UTC_TEST_PASSWORD"])
    login_page.submit()
    assert_authenticated(login_page.driver)


def test_lg13_remember_checkbox_toggles(login_page):
    initial = login_page.is_remember_selected()
    login_page.set_remember(not initial)
    assert login_page.is_remember_selected() is not initial
    login_page.set_remember(initial)
    assert login_page.is_remember_selected() is initial


def test_lg14_remember_session_after_browser_restart(pytestconfig):
    data = require_env(
        "UTC_TEST_USERNAME", "UTC_TEST_PASSWORD",
        "UTC_AUTH_IDENTITY_SELECTOR", "UTC_AUTH_IDENTITY_TEXT",
        "UTC_PROTECTED_URL", "UTC_REMEMBER_POLICY",
    )
    if data["UTC_REMEMBER_POLICY"].lower() != "retain":
        pytest.skip("Not Applicable: configured remember policy is not retain")
    with tempfile.TemporaryDirectory(prefix="utc-login-") as profile:
        def open_browser():
            options = webdriver.ChromeOptions()
            options.add_argument("--window-size=1440,900")
            options.add_argument(f"--user-data-dir={profile}")
            if pytestconfig.getoption("--headless"):
                options.add_argument("--headless=new")
            return webdriver.Chrome(options=options)

        first = open_browser()
        try:
            page = LoginPage(first).open()
            page.set_remember(True)
            page.login(data["UTC_TEST_USERNAME"], data["UTC_TEST_PASSWORD"])
            assert_authenticated(first)
        finally:
            first.quit()

        second = open_browser()
        try:
            second.get(data["UTC_PROTECTED_URL"])
            assert_authenticated(second)
        finally:
            second.quit()


def test_lg15_forgot_password_navigation(login_page):
    login_page.forgot_password()
    WebDriverWait(login_page.driver, 10).until(
        EC.url_contains("/Login/GetPass")
    )
    assert login_page.driver.current_url.endswith("/Login/GetPass")
    recovery = login_page.driver.find_element(By.TAG_NAME, "body").text
    assert "Trở lại đăng nhập?" in recovery
    assert login_page.driver.find_elements(By.CSS_SELECTOR, "input")
