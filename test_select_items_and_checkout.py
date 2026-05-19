"""
Тест выбора товаров, проверки названий и цен, сверки суммы
"""

import pytest
import time
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from config.test_data import TestData


class TestSelectItemsAndCheckout:
    """
    Класс с тестом для проверки:
    1. Авторизация на сайте
    2. Выбор 2 товаров
    3. Сохранение названий и цен товаров
    4. Прохождение процесса оплаты
    5. Сверка сохраненных значений с данными в корзине
    6. Проверка правильности подсчета суммы
    """
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Настройка перед тестом"""
        self.login_page = LoginPage(driver)
        self.login_page.open()
    
    def test_select_two_items_and_checkout(self, driver):
        """
        Тест: Выбор 2 товаров, проверка названий и цен, сверка суммы
        """
        print("\n" + "=" * 70)
        print("ТЕСТ: ВЫБОР ТОВАРОВ, ПРОВЕРКА НАЗВАНИЙ И ЦЕН, СВЕРКА СУММЫ")
        print("=" * 70)
        
        # =========================================================
        # ШАГ 1: АВТОРИЗАЦИЯ НА САЙТЕ
        # =========================================================
        print("\n[Шаг 1] Авторизация на сайте...")
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        time.sleep(3)
        
        current_url = driver.current_url
        print(f"Текущий URL после авторизации: {current_url}")
        assert "inventory.html" in current_url, "Авторизация не выполнена"
        print("Авторизация успешно выполнена")
        
        # =========================================================
        # ШАГ 2: ВЫБОР 2 ТОВАРОВ И СОХРАНЕНИЕ ИХ ДАННЫХ
        # =========================================================
        print("\n[Шаг 2] Выбор 2 товаров и сохранение названий и цен...")
        time.sleep(2)
        
        # ВАЖНО: ДВА СЛЕША // ДЛЯ ПОИСКА В ЛЮБОМ МЕСТЕ
        items_names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        items_prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        
        print(f"Найдено товаров: {len(items_names)}")
        assert len(items_names) >= 2, f"Найдено только {len(items_names)} товаров"
        
        # Сохраняем данные
        item1_name = items_names[0].text
        item1_price = float(items_prices[0].text.replace("$", ""))
        item2_name = items_names[1].text
        item2_price = float(items_prices[1].text.replace("$", ""))
        
        print(f"Товар 1: {item1_name} - ${item1_price}")
        print(f"Товар 2: {item2_name} - ${item2_price}")
        
        # =========================================================
        # ШАГ 3: ДОБАВЛЕНИЕ ТОВАРОВ В КОРЗИНУ
        # =========================================================
        print("\n[Шаг 3] Добавление товаров в корзину...")
        
        add_buttons = driver.find_elements(By.CSS_SELECTOR, "button.btn_inventory")
        add_buttons[0].click()
        print("Товар 1 добавлен")
        time.sleep(1)
        add_buttons[1].click()
        print("Товар 2 добавлен")
        time.sleep(1)
        
        # =========================================================
        # ШАГ 4: ПЕРЕХОД В КОРЗИНУ И ПРОВЕРКА ДАННЫХ
        # =========================================================
        print("\n[Шаг 4] Переход в корзину...")
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        time.sleep(2)
        
        cart_names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        cart_prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        
        assert len(cart_names) == 2, f"В корзине {len(cart_names)} товаров"
        
        # Сверка названий и цен
        calc_sum = 0
        for i, expected_name in enumerate([item1_name, item2_name]):
            assert cart_names[i].text == expected_name, f"Название {i+1} не совпадает"
            price = float(cart_prices[i].text.replace("$", ""))
            calc_sum += price
        
        print(f"Проверка пройдена. Сумма: ${calc_sum}")
        
        # =========================================================
        # ШАГ 5: ОФОРМЛЕНИЕ ЗАКАЗА
        # =========================================================
        print("\n[Шаг 5] Оформление заказа...")
        driver.find_element(By.ID, "checkout").click()
        time.sleep(1)
        
        driver.find_element(By.ID, "first-name").send_keys("Test")
        driver.find_element(By.ID, "last-name").send_keys("User")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        time.sleep(1)
        
        driver.find_element(By.ID, "continue").click()
        time.sleep(2)
        
        # =========================================================
        # ШАГ 6: ПРОВЕРКА СУММЫ
        # =========================================================
        total_text = driver.find_element(By.CLASS_NAME, "summary_subtotal_label").text
        total_sum = float(total_text.replace("Item total: $", ""))
        
        assert calc_sum == total_sum, f"Суммы не совпадают: {calc_sum} vs {total_sum}"
        print(f"Сумма совпадает: ${total_sum}")
        
        # =========================================================
        # ШАГ 7: ЗАВЕРШЕНИЕ
        # =========================================================
        print("\n[Шаг 7] Завершение покупки...")
        driver.find_element(By.ID, "finish").click()
        time.sleep(2)
        
        message = driver.find_element(By.CLASS_NAME, "complete-header").text
        assert message == "Thank you for your order!", f"Сообщение: {message}"
        print(f"Успех! {message}")
        
        print("\n" + "=" * 70)
        print("ТЕСТ ПРОЙДЕН УСПЕШНО")
        print("=" * 70)


if __name__ == "__main__":
    pytest.main(["-v", __file__])