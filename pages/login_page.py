from selenium.webdriver.common.by import By

from base.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://vanphongdientu.utc.edu.vn/Login"

    _USERNAME = (By.NAME, "username")
    _PASSWORD = (By.NAME, "userpwd")

    _SUBMIT = (
        By.CSS_SELECTOR,
        "input.submit_login",
    )

    _REMEMBER_INPUT = (
        By.ID,
        "persistent",
    )

    _REMEMBER_LABEL = (
        By.CSS_SELECTOR,
        "label.check",
    )

    _FORGOT_PASSWORD = (
        By.CSS_SELECTOR,
        "a[href='/Login/GetPass']",
    )

    _EMAIL_LOGIN = (
        By.XPATH,
        "//a[contains(normalize-space(.), 'e-mail UTC')]",
    )

    def open(self):
        self.open_url(self.URL)

        # Chờ các điều khiển chính trước khi thao tác.
        self.visible(self._USERNAME)
        self.visible(self._PASSWORD)
        self.visible(self._SUBMIT)

        return self

    def form_visibility(self):
        return {
            "username": self.is_visible(self._USERNAME),
            "password": self.is_visible(self._PASSWORD),
            "submit": self.is_visible(self._SUBMIT),
            "remember": self.is_visible(self._REMEMBER_LABEL),
            "forgot_password": self.is_visible(
                self._FORGOT_PASSWORD
            ),
            "email_login": self.is_visible(self._EMAIL_LOGIN),
        }

    def fill_credentials(self, username, password):
        self.type_text(self._USERNAME, username)
        self.type_text(self._PASSWORD, password)

    def submit(self):
        self.click(self._SUBMIT)

    def login(self, username, password):
        self.fill_credentials(username, password)
        self.submit()

    def password_type(self):
        return self.visible(
            self._PASSWORD
        ).get_dom_attribute("type")

    def is_remember_selected(self):
        return self.driver.find_element(
            *self._REMEMBER_INPUT
        ).is_selected()

    def set_remember(self, selected):
        if self.is_remember_selected() != selected:
            self.click(self._REMEMBER_LABEL)

        self.wait.until(
            lambda driver:
                self.is_remember_selected() == selected
        )