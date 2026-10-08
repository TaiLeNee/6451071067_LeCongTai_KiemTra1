import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def require_env(*names):
    values = {name: os.getenv(name, '') for name in names}
    missing = [name for name, value in values.items() if not value.strip()]
    if missing:
        pytest.skip('Blocked: missing ' + ', '.join(missing))
    return values


def assert_authenticated(driver):
    values = require_env('UTC_AUTH_IDENTITY_SELECTOR', 'UTC_AUTH_IDENTITY_TEXT')
    marker = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, values['UTC_AUTH_IDENTITY_SELECTOR'])
        )
    )
    assert values['UTC_AUTH_IDENTITY_TEXT'] in marker.text


def assert_rejected(login_page, expected_text=None):
    error = login_page.error_text()
    assert error, 'No visible login error'
    if expected_text is not None:
        assert expected_text in error
    assert login_page.driver.current_url.rstrip('/').endswith('/Login')
    return error
