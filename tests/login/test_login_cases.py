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
