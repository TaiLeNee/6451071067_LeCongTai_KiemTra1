from tests.login.support import assert_authenticated, require_env


def test_lg03_valid_credentials_open_account(login_page):
    data = require_env(
        "UTC_TEST_USERNAME", "UTC_TEST_PASSWORD",
        "UTC_AUTH_IDENTITY_SELECTOR", "UTC_AUTH_IDENTITY_TEXT",
    )
    login_page.login(data["UTC_TEST_USERNAME"], data["UTC_TEST_PASSWORD"])
    assert_authenticated(login_page.driver)
