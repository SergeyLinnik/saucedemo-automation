"""
Тест добавления всех товаров в корзину и скролла до последнего элемента
"""

import pytest
import time
from pages.login_page import LoginPage
from config.test_data import TestData


class TestAddToCartAndScroll:
    """
    Класс с тестом для добавления товаров в корзину и скролла
    """
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Настройка перед тестом"""
        self.login_page = LoginPage(driver)
        self.login_page.open()
    
    def test_add_all_items_to_cart_and_scroll(self, driver):
        """
        Тест:
        1. Авторизоваться на сайте
        2. Добавить все товары в корзину
        3. Перейти в корзину
        4. Используя метод move_to_element, скроллить до последнего элемента в корзине
        """
        print("\n" + "=" * 60)
        print("ТЕСТ: ДОБАВЛЕНИЕ ВСЕХ ТОВАРОВ В КОРЗИНУ И СКРОЛЛ")
        print("=" * 60)
        
        # Шаг 1: Авторизация на сайте
        print("\n[Шаг 1] Авторизация на сайте...")
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        print("Авторизация выполнена успешно")
        
        self.login_page.wait_for_url_contains(TestData.SUCCESS_URL_PART)
        assert TestData.SUCCESS_URL_PART in driver.current_url, \
            "Не удалось перейти на страницу каталога"
        print("Страница каталога загружена")
        
        # Шаг 2: Добавление всех товаров в корзину
        print("\n[Шаг 2] Добавление всех товаров в корзину...")
        self.login_page.add_all_items_to_cart()
        
        cart_count = self.login_page.get_cart_item_count()
        assert cart_count > 0, "Товары не были добавлены в корзину"
        print(f"В корзину добавлено {cart_count} товаров")
        
        # Шаг 3: Переход в корзину
        print("\n[Шаг 3] Переход в корзину...")
        self.login_page.go_to_cart()
        
        time.sleep(2)
        assert "cart.html" in driver.current_url, "Не удалось перейти на страницу корзины"
        print("Страница корзины загружена")
        
        # Шаг 4: Скроллинг до последнего элемента в корзине с помощью move_to_element
        print("\n[Шаг 4] Скроллинг до последнего элемента в корзине...")
        self.login_page.scroll_to_last_cart_item()
        print("Скроллинг до последнего элемента выполнен")
        
        cart_items = self.login_page.get_cart_items()
        assert len(cart_items) > 0, "Корзина пуста"
        print(f"В корзине отображается {len(cart_items)} товаров")
        
        last_item = cart_items[-1]
        assert last_item.is_displayed(), "Последний элемент не отображается после скролла"
        print("Последний элемент корзины успешно отображается после скролла")
        
        print("\n" + "=" * 60)
        print("РЕЗУЛЬТАТ ТЕСТА:")
        print("=" * 60)
        print("Авторизация выполнена успешно")
        print(f"Добавлено {cart_count} товаров в корзину")
        print("Выполнен переход в корзину")
        print("Выполнен скроллинг до последнего элемента с помощью move_to_element")
        print("=" * 60)
        print("[ТЕСТ] ПРОЙДЕН")


if __name__ == "__main__":
    pytest.main(["-v", __file__])