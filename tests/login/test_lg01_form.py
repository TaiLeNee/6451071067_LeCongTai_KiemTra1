def test_lg01_login_form_visible(login_page):
    visibility = login_page.form_visibility()

    for name, is_visible in visibility.items():
        assert is_visible, (
            f"Điều khiển '{name}' không hiển thị"
        )