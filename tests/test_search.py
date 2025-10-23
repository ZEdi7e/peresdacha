import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://demo-opencart.ru/index.php?route=common/home"

@pytest.mark.order(3)
@allure.description("""
Цель: Проверить поиск по ключевым словам с существующими результатами.
Ожидаемый результат: Отображаются релевантные товары (например, для "iPhone" - продукты с "iPhone" в названии).
""")
def test_search_with_results(driver):
    driver.get(BASE_URL)
    driver.find_element(By.NAME, "search").send_keys("iPhone")
    driver.find_element(By.CSS_SELECTOR, "span.input-group-btn button").click()
    
    wait = WebDriverWait(driver, 10)
    results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-layout")))
    assert len(results) > 0, "Результаты поиска не найдены"
    first_result = driver.find_element(By.CSS_SELECTOR, "div.caption h4 a")
    assert "Mac" in first_result.text, "Результаты не соответствуют запросу"

@pytest.mark.order(3)
@allure.description("""
Цель: Проверить поведение при отсутствии результатов поиска.
Ожидаемый результат: Нет товаров, которые соответствуют критериям поиска.
""")
def test_search_no_results(driver):
    driver.get(BASE_URL)
    driver.find_element(By.NAME, "search").send_keys("PC")
    driver.find_element(By.CSS_SELECTOR, "span.input-group-btn button").click()
    
    wait = WebDriverWait(driver, 10)
    
    # Ждем загрузки страницы с результатами поиска
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    
    # Ищем сообщение об отсутствии результатов
    no_results_message = wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Нет товаров')]")))
    
    assert "Нет товаров, которые соответствуют критериям поиска." in no_results_message.text, "Сообщение об отсутствии результатов не отображено"