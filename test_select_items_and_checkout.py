"""
Тест выбора товаров, проверки названий и цен, сверки суммы
"""

import pytest
import time
from typing import List, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
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
    def setup(self, driver: WebDriver) -> None:
        """
        Настройка перед тестом
        
        Args:
            driver: Экземпляр веб-драйвера
        """
        self.login_page: LoginPage = LoginPage(driver)
        self.login_page.open()
    
    def test_select_two_items_and_checkout(self, driver: WebDriver) -> None:
        """
        Тест: Выбор 2 товаров, проверка названий и цен, сверка суммы
        
        Args:
            driver: Экземпляр веб-драйвера
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
        
        # Проверка успешной авторизации по URL
        current_url: str = driver.current_url
        print(f"Текущий URL после авторизации: {current_url}")
        assert "inventory.html" in current_url, "Авторизация не выполнена"
        print("Авторизация успешно выполнена")
        
        # =========================================================
        # ШАГ 2: ВЫБОР 2 ТОВАРОВ И СОХРАНЕНИЕ ИХ ДАННЫХ
        # =========================================================
        print("\n[Шаг 2] Выбор 2 товаров и сохранение названий и цен...")
        time.sleep(2)
        
        # Получаем список всех названий и цен товаров
        items_names: List = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        items_prices: List = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        
        print(f"Найдено товаров: {len(items_names)}")
        
        # Проверяем, что товары есть
        assert len(items_names) >= 2, f"Найдено только {len(items_names)} товаров"
        
        # Сохраняем данные первого товара (индекс 0)
        item_1_name: str = items_names[0].text
        item_1_price_text: str = items_prices[0].text.replace("$", "")
        item_1_price: float = float(item_1_price_text)
        
        # Сохраняем данные второго товара (индекс 1)
        item_2_name: str = items_names[1].text
        item_2_price_text: str = items_prices[1].text.replace("$", "")
        item_2_price: float = float(item_2_price_text)
        
        # Список выбранных товаров для удобства
        selected_items: List[dict] = [
            {"name": item_1_name, "price": item_1_price},
            {"name": item_2_name, "price": item_2_price}
        ]
        
        print("\n--- СОХРАНЕННЫЕ ДАННЫЕ ТОВАРОВ ---")
        for i, item in enumerate(selected_items, 1):
            print(f"Товар {i}: {item['name']} - ${item['price']}")
        
        # =========================================================
        # ШАГ 3: ДОБАВЛЕНИЕ ТОВАРОВ В КОРЗИНУ
        # =========================================================
        print("\n[Шаг 3] Добавление товаров в корзину...")
        
        # Находим все кнопки "Add to cart"
        add_buttons: List = driver.find_elements(By.CSS_SELECTOR, "button.btn_inventory")
        
        # Добавляем первый товар
        add_buttons[0].click()
        print("Товар 1 добавлен в корзину")
        time.sleep(1)
        
        # Добавляем второй товар
        add_buttons[1].click()
        print("Товар 2 добавлен в корзину")
        time.sleep(1)
        
        # =========================================================
        # ШАГ 4: ПЕРЕХОД В КОРЗИНУ И ПРОВЕРКА ДАННЫХ
        # =========================================================
        print("\n[Шаг 4] Переход в корзину...")
        
        # Переход на страницу корзины
        cart_link: WebDriver = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_link.click()
        time.sleep(2)
        
        # Получаем товары в корзине
        cart_items_names: List = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        cart_items_prices: List = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        
        # Проверяем количество товаров в корзине
        cart_items_count: int = len(cart_items_names)
        print(f"В корзине товаров: {cart_items_count}")
        assert cart_items_count == 2, f"В корзине {cart_items_count} товаров, ожидалось 2"
        
        # Проверка названий товаров в корзине
        print("\n--- ПРОВЕРКА НАЗВАНИЙ ТОВАРОВ В КОРЗИНЕ ---")
        for i, expected_item in enumerate(selected_items):
            actual_name: str = cart_items_names[i].text
            assert actual_name == expected_item["name"], \
                f"Название товара {i + 1} не совпадает. Ожидалось: {expected_item['name']}, Получено: {actual_name}"
            print(f"Товар {i + 1}: название совпадает - {actual_name}")
        
        # Проверка цен товаров в корзине и расчет суммы
        print("\n--- ПРОВЕРКА ЦЕН ТОВАРОВ В КОРЗИНЕ ---")
        calculated_sum: float = 0.0
        for i, expected_item in enumerate(selected_items):
            price_text: str = cart_items_prices[i].text.replace("$", "")
            actual_price: float = float(price_text)
            assert actual_price == expected_item["price"], \
                f"Цена товара {i + 1} не совпадает. Ожидалось: ${expected_item['price']}, Получено: ${actual_price}"
            print(f"Товар {i + 1}: цена совпадает - ${actual_price}")
            calculated_sum += actual_price
        
        print(f"\nРассчитанная сумма товаров: ${calculated_sum}")
        
        # =========================================================
        # ШАГ 5: ПРОЦЕСС ОФОРМЛЕНИЯ ЗАКАЗА (CHECKOUT)
        # =========================================================
        print("\n[Шаг 5] Процесс оформления заказа...")
        
        # Нажатие кнопки Checkout
        checkout_button: WebDriver = driver.find_element(By.ID, "checkout")
        checkout_button.click()
        print("Нажата кнопка Checkout")
        time.sleep(1)
        
        # Заполнение информации о покупателе
        first_name_field: WebDriver = driver.find_element(By.ID, "first-name")
        last_name_field: WebDriver = driver.find_element(By.ID, "last-name")
        postal_code_field: WebDriver = driver.find_element(By.ID, "postal-code")
        
        first_name_field.send_keys("Test")
        last_name_field.send_keys("User")
        postal_code_field.send_keys("12345")
        print("Заполнены данные покупателя: Test User, 12345")
        time.sleep(1)
        
        # Нажатие кнопки Continue
        continue_button: WebDriver = driver.find_element(By.ID, "continue")
        continue_button.click()
        print("Нажата кнопка Continue")
        time.sleep(2)
        
        # =========================================================
        # ШАГ 6: ПРОВЕРКА СУММЫ НА СТРАНИЦЕ ОПЛАТЫ
        # =========================================================
        print("\n[Шаг 6] Проверка суммы на странице оплаты...")
        
        # Получение общей суммы из системы
        total_element: WebDriver = driver.find_element(By.CLASS_NAME, "summary_subtotal_label")
        total_text: str = total_element.text.replace("Item total: $", "")
        total_sum: float = float(total_text)
        print(f"Общая сумма в системе: ${total_sum}")
        
        # Сверка рассчитанной суммы с суммой в системе
        assert calculated_sum == total_sum, \
            f"Сумма не совпадает! Рассчитано: ${calculated_sum}, В системе: ${total_sum}"
        print(f"Сумма совпадает: рассчитано ${calculated_sum}, в системе ${total_sum}")
        
        # =========================================================
        # ШАГ 7: ЗАВЕРШЕНИЕ ПОКУПКИ
        # =========================================================
        print("\n[Шаг 7] Завершение покупки...")
        
        # Нажатие кнопки Finish
        finish_button: WebDriver = driver.find_element(By.ID, "finish")
        finish_button.click()
        print("Нажата кнопка Finish")
        time.sleep(2)
        
        # Проверка успешного завершения заказа
        complete_message: WebDriver = driver.find_element(By.CLASS_NAME, "complete-header")
        message_text: str = complete_message.text
        assert message_text == "Thank you for your order!", \
            f"Сообщение не совпадает: {message_text}"
        print(f"Покупка успешно завершена! Сообщение: {message_text}")
        
        # =========================================================
        # ВЫВОД РЕЗУЛЬТАТА
        # =========================================================
        print("\n" + "=" * 70)
        print("РЕЗУЛЬТАТ ТЕСТА:")
        print("=" * 70)
        print("Авторизация на сайте - ВЫПОЛНЕНО")
        print(f"Выбраны товары: {item_1_name} (${item_1_price}), {item_2_name} (${item_2_price})")
        print("Названия и цены сохранены в переменные")
        print("Названия товаров в корзине совпадают с сохраненными")
        print("Цены товаров в корзине совпадают с сохраненными")
        print(f"Рассчитанная сумма (${calculated_sum}) совпадает с суммой в системе (${total_sum})")
        print("Процесс оплаты пройден успешно")
        print("=" * 70)
        print("[ТЕСТ] ПРОЙДЕН")


if __name__ == "__main__":
    pytest.main(["-v", __file__])