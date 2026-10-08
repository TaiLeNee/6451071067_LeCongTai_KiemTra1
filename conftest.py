import pytest
from selenium import webdriver

from pages.login_page import LoginPage


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        help="Chạy Chrome không hiện cửa sổ",
    )


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1440,900")

    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")

    browser = webdriver.Chrome(options=options)

    try:
        yield browser
    finally:
        browser.quit()


@pytest.fixture
def login_page(driver):
    page = LoginPage(driver)
    page.open()
    return page