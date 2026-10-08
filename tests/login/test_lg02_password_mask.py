def test_lg02_password_is_masked(login_page):
    password = "sample-password"
    login_page.fill_credentials("test_validation", password)

    assert login_page.password_type() == "password"
    assert login_page.password_value() == password
