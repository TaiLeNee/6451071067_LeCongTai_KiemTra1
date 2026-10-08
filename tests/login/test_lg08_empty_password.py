from tests.login.support import assert_rejected


def test_lg08_password_empty(login_page):
    login_page.fill_credentials("test_validation", "")
    login_page.submit()
    assert_rejected(login_page, "Bạn chưa nhập mật khẩu")
