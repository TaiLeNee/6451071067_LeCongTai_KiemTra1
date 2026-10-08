from tests.login.support import assert_rejected, require_env


def test_lg04_wrong_password_is_rejected(login_page):
    data = require_env(
        "UTC_TEST_USERNAME", "UTC_TEST_PASSWORD",
        "UTC_WRONG_PASSWORD", "UTC_INVALID_CREDENTIALS_TEXT",
    )
    assert data["UTC_WRONG_PASSWORD"] != data["UTC_TEST_PASSWORD"]
    login_page.login(data["UTC_TEST_USERNAME"], data["UTC_WRONG_PASSWORD"])
    assert_rejected(login_page, data["UTC_INVALID_CREDENTIALS_TEXT"])
