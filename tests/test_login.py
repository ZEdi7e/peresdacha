import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://demo-opencart.ru/index.php?route=common/home"

@pytest.mark.order(2)
@allure.description("""
Цель: Проверить успешный вход с корректными учетными данными.
Ожидаемый результат: Моя учетная запись.
""")
def test_successful_login(driver):
    driver.get(BASE_URL)
    driver.find_element(By.LINK_TEXT, "Личный кабинет").click()
    driver.find_element(By.LINK_TEXT, "Авторизация").click()
    
    email = "egor@mail.ru"
    password = "egor290307!!"
    
    driver.find_element(By.ID, "input-email").send_keys(email)
    driver.find_element(By.ID, "input-password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary").click()
    
    wait = WebDriverWait(driver, 10)
    account_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2")))
    assert "Моя учетная запись" in account_title.text, "Не удалось войти в аккаунт"

@pytest.mark.order(2)
@allure.description("""
Цель: Проверить вход с некорректными учетными данными.
Ожидаемый результат: Неправильно заполнены поле E-Mail и/или пароль!".
""")
def test_invalid_login(driver):
    driver.get(BASE_URL)
    driver.find_element(By.LINK_TEXT, "Личный кабинет").click()
    driver.find_element(By.LINK_TEXT, "Авторизация").click()
    
    driver.find_element(By.ID, "input-email").send_keys("nouser@mail.ru")
    driver.find_element(By.ID, "input-password").send_keys("nouserno123!")
    driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary").click()
    
    wait = WebDriverWait(driver, 10)
    error_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert.alert-danger")))

    assert "Неправильно заполнены поле E-Mail и/или пароль!" in error_message.text, "Сообщение об ошибке не отображено"
