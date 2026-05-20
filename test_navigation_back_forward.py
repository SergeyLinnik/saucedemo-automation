"""
Тест навигации с использованием методов back() и forward()
Авторизация -> Выбор товара -> Переход в корзину -> Возврат в каталог (back) -> Снова в корзину (forward)
"""

import pytest
import time
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.login_page import LoginPage
from config.test_data import TestData


class TestNavigationBackForward:
    """
    Класс с тестом для проверки навигации:
    1. Авторизация на сайте
    2. Выбор товара
    3. Переход в корзину
    4. Возврат на страницу каталога (метод back)
    5. Снова переход в корзину (метод forward)
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
    
    def test_navigation_back_and_forward(self, driver: WebDriver) -> None:
        """
        Тест: Авторизация -> Выбор товара -> Корзина -> Назад (back) -> Вперед (forward)
        
        Args:
            driver: Экземпляр веб-драйвера
        """
        print("\n" + "=" * 70)
        print("ТЕСТ: НАВИГАЦИЯ С МЕТОДАМИ BACK() И FORWARD()")
        print("=" * 70)
        
        # =========================================================
        # ШАГ 1: АВТОРИЗАЦИЯ НА САЙТЕ
        # =========================================================
        print("\n[Шаг 1] Авторизация на сайте...")
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        time.sleep(2)
        
        current_url: str = driver.current_url
        assert "inventory.html" in current_url, "Авторизация не выполнена"
        print(f"Страница каталога: {current_url}")
        
        # =========================================================
        # ШАГ 2: ВЫБОР ТОВАРА И ДОБАВЛЕНИЕ В КОРЗИНУ
        # =========================================================
        print("\n[Шаг 2] Выбор товара и добавление в корзину...")
        
        # Получаем название первого товара
        first_item_name: str = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        print(f"Выбран товар: {first_item_name}")
        
        # Добавляем товар в корзину
        add_button = driver.find_element(By.CSS_SELECTOR, "button.btn_inventory")
        add_button.click()
        print("Товар добавлен в корзину")
        time.sleep(1)
        
        # =========================================================
        # ШАГ 3: ПЕРЕХОД В КОРЗИНУ
        # =========================================================
        print("\n[Шаг 3] Переход в корзину...")
        cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_link.click()
        time.sleep(2)
        
        cart_url: str = driver.current_url
        assert "cart.html" in cart_url, "Не удалось перейти в корзину"
        print(f"Страница корзины: {cart_url}")
        
        # Проверяем, что товар в корзине
        cart_item = driver.find_element(By.CLASS_NAME, "inventory_item_name")
        assert cart_item.text == first_item_name, "Товар не найден в корзине"
        print(f"В корзине товар: {cart_item.text}")
        
        # =========================================================
        # ШАГ 4: ВОЗВРАТ НА СТРАНИЦУ КАТАЛОГА (МЕТОД BACK)
        # =========================================================
        print("\n[Шаг 4] Возврат на страницу каталога с помощью метода back()...")
        
        # Запоминаем URL до возврата
        before_back_url: str = driver.current_url
        print(f"URL до back(): {before_back_url}")
        
        # Используем метод back() для возврата
        self.login_page.go_back()
        
        # Проверяем, что вернулись на страницу каталога
        after_back_url: str = driver.current_url
        print(f"URL после back(): {after_back_url}")
        
        assert "inventory.html" in after_back_url, \
            f"Не удалось вернуться на страницу каталога. URL: {after_back_url}"
        assert after_back_url != before_back_url, "URL не изменился после back()"
        print("Успешный возврат на страницу каталога через back()")
        
        # =========================================================
        # ШАГ 5: СНОВА ПЕРЕХОД В КОРЗИНУ (МЕТОД FORWARD)
        # =========================================================
        print("\n[Шаг 5] Переход вперед в корзину с помощью метода forward()...")
        
        # Запоминаем URL до перехода вперед
        before_forward_url: str = driver.current_url
        print(f"URL до forward(): {before_forward_url}")
        
        # Используем метод forward() для перехода вперед
        self.login_page.go_forward()
        
        # Проверяем, что перешли на страницу корзины
        after_forward_url: str = driver.current_url
        print(f"URL после forward(): {after_forward_url}")
        
        assert "cart.html" in after_forward_url, \
            f"Не удалось перейти на страницу корзины. URL: {after_forward_url}"
        assert after_forward_url != before_forward_url, "URL не изменился после forward()"
        print("Успешный переход на страницу корзины через forward()")
        
        # =========================================================
        # ШАГ 6: ПРОВЕРКА, ЧТО ТОВАР ОСТАЛСЯ В КОРЗИНЕ
        # =========================================================
        print("\n[Шаг 6] Проверка, что товар остался в корзине...")
        
        cart_item_again = driver.find_element(By.CLASS_NAME, "inventory_item_name")
        assert cart_item_again.text == first_item_name, "Товар не найден в корзине после forward()"
        print(f"В корзине по-прежнему товар: {cart_item_again.text}")
        
        # =========================================================
        # ВЫВОД РЕЗУЛЬТАТА
        # =========================================================
        print("\n" + "=" * 70)
        print("РЕЗУЛЬТАТ ТЕСТА:")
        print("=" * 70)
        print("Авторизация на сайте - ВЫПОЛНЕНО")
        print(f"Выбран товар: {first_item_name}")
        print("Переход в корзину - ВЫПОЛНЕНО")
        print("Возврат на страницу каталога через back() - ВЫПОЛНЕНО")
        print("Переход вперед в корзину через forward() - ВЫПОЛНЕНО")
        print("Товар сохранился в корзине после навигации")
        print("=" * 70)
        print("[ТЕСТ] ПРОЙДЕН")


class TestMultipleNavigation:
    """
    Дополнительный тест для проверки множественной навигации
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
    
    def test_multiple_back_and_forward(self, driver: WebDriver) -> None:
        """
        Тест: Множественные переходы back() и forward()
        
        Args:
            driver: Экземпляр веб-драйвера
        """
        print("\n" + "=" * 70)
        print("ТЕСТ: МНОЖЕСТВЕННЫЕ ПЕРЕХОДЫ BACK() И FORWARD()")
        print("=" * 70)
        
        # Авторизация
        print("\n[Шаг 1] Авторизация...")
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        time.sleep(2)
        print(f"Стартовая страница: {driver.current_url}")
        
        # Переход в корзину (пустую)
        print("\n[Шаг 2] Переход в корзину...")
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        time.sleep(1)
        print(f"Корзина: {driver.current_url}")
        
        # Возврат в каталог
        print("\n[Шаг 3] Возврат в каталог через back()...")
        self.login_page.go_back()
        print(f"Каталог: {driver.current_url}")
        
        # Снова в корзину
        print("\n[Шаг 4] Снова в корзину через forward()...")
        self.login_page.go_forward()
        print(f"Корзина: {driver.current_url}")
        
        # Проверка
        assert "cart.html" in driver.current_url, "Не удалось вернуться в корзину"
        print("\nМножественные переходы back() и forward() успешно выполнены")
        
        print("\n[ТЕСТ] ПРОЙДЕН")


if __name__ == "__main__":
    pytest.main(["-v", __file__])