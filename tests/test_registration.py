import pytest
import allure
import uuid
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://demo-opencart.ru/index.php?route=common/home"

@pytest.mark.order(1)
@allure.description("""
Цель: Проверить успешную регистрацию новой учетной записи.
Ожидаемый результат: Ваша учетная запись создана!".
""")
def test_successful_registration(driver):
    driver.get(BASE_URL)
    driver.find_element(By.LINK_TEXT, "Личный кабинет").click()
    driver.find_element(By.LINK_TEXT, "Регистрация").click()
    
    unique_email = f"ffart0609{uuid.uuid4().hex[:10]}@mail.ru"
    
    driver.find_element(By.ID, "input-firstname").send_keys("renat")
    driver.find_element(By.ID, "input-lastname").send_keys("yushvaev")
    driver.find_element(By.ID, "input-email").send_keys(unique_email)
    driver.find_element(By.ID, "input-telephone").send_keys("89166445887")
    driver.find_element(By.ID, "input-password").send_keys("renat220806!")
    driver.find_element(By.ID, "input-confirm").send_keys("renat220806!")
    driver.find_element(By.NAME, "agree").click()
    driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary").click()
    
    wait = WebDriverWait(driver, 10)
    
    try:
        success_message = wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Поздравляем')]")))
        assert "Поздравляем! Ваш Личный Кабинет был успешно создан." in success_message.text
        print("Успешная регистрация подтверждена!")
    except:
        page_source = driver.page_source
        if "Поздравляем" in page_source or "успешно создан" in page_source:
            print("Регистрация успешна (текст найден в странице)")
        else:
            error_elements = driver.find_elements(By.CLASS_NAME, "text-danger")
            if error_elements:
                for error in error_elements:
                    print(f"Ошибка: {error.text}")
            raise AssertionError("Сообщение об успешной регистрации не найдено")
    
    current_url = driver.current_url
    if "account/success" in current_url or "route=account/success" in current_url:
        print("Находимся на странице успешной регистрации")

@pytest.mark.order(1)
@allure.description("""
Цель: Проверить повторную регистрацию с существующим логином.
Ожидаемый результат: Данный E-Mail уже зарегистрирован!".
""")
def test_duplicate_registration(driver):
    driver.get(BASE_URL)
    driver.find_element(By.LINK_TEXT, "Личный кабинет").click()
    driver.find_element(By.LINK_TEXT, "Регистрация").click()
    
    existing_email = "rezmeritsaea22@st.ithub.ru"  
    
    driver.find_element(By.ID, "input-firstname").send_keys("renat")
    driver.find_element(By.ID, "input-lastname").send_keys("yushvaev")
    driver.find_element(By.ID, "input-email").send_keys(existing_email)
    driver.find_element(By.ID, "input-telephone").send_keys("89166445887")
    driver.find_element(By.ID, "input-password").send_keys("renat220806!")
    driver.find_element(By.ID, "input-confirm").send_keys("renat220806!")
    driver.find_element(By.NAME, "agree").click()
    driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary").click()
    
    wait = WebDriverWait(driver, 10)
    
    error_message = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.alert.alert-danger")))
    
    expected_error = "Данный E-Mail уже зарегистрирован!"
    actual_error = error_message.text.strip()
    

    assert expected_error in actual_error, f"Ожидалось: '{expected_error}', Получено: '{actual_error}'"
