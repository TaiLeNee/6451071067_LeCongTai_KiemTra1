from tests.login.support import assert_rejected


def test_lg09_whitespace_username(login_page):
    login_page.fill_credentials("   ", "sample-password")
    login_page.submit()
    assert_rejected(login_page, "Tài khoản hoặc mật khẩu không đúng.")
