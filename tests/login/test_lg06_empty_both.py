from tests.login.support import assert_rejected


def test_lg06_both_fields_empty(login_page):
    login_page.fill_credentials("", "")
    login_page.submit()
    assert_rejected(login_page, "Bạn chưa nhập tên đăng nhập")
