from tests.login.support import assert_rejected, require_env


def test_lg05_unknown_account_is_rejected(login_page):
    data = require_env(
        "UTC_UNKNOWN_USERNAME", "UTC_UNKNOWN_PASSWORD",
        "UTC_INVALID_CREDENTIALS_TEXT",
    )
    login_page.login(data["UTC_UNKNOWN_USERNAME"], data["UTC_UNKNOWN_PASSWORD"])
    assert_rejected(login_page, data["UTC_INVALID_CREDENTIALS_TEXT"])
