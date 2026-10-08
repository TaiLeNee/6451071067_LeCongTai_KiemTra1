from tests.login.support import assert_rejected


def test_lg07_username_empty(login_page):
    login_page.fill_credentials("", "sample-password")
    login_page.submit()
    assert_rejected(login_page, "Bạn chưa nhập tên đăng nhập")
