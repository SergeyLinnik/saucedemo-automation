"""
Тест создания скриншота страницы каталога
"""

import pytest
import os
from pages.login_page import LoginPage
from config.test_data import TestData


class TestCatalogScreenshot:
    """
    Класс с тестом для создания скриншота страницы каталога
    """
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """Настройка перед тестом"""
        self.login_page = LoginPage(driver)
        self.login_page.open()
    
    def test_catalog_page_screenshot(self, driver):
        """
        Тест: Создание скриншота страницы каталога
        """
        print("\n[Тест] Создание скриншота страницы каталога")
        
        # 1. Выполняем авторизацию
        self.login_page.login(TestData.VALID_USERNAME, TestData.VALID_PASSWORD)
        print("Авторизация выполнена")
        
        # 2. Ожидаем загрузки страницы каталога
        self.login_page.wait_for_url_contains(TestData.SUCCESS_URL_PART)
        assert TestData.SUCCESS_URL_PART in driver.current_url, \
            "Не удалось перейти на страницу каталога"
        print("Страница каталога загружена")
        
        # 3. Делаем скриншот страницы каталога
        screenshot_path = self.login_page.take_catalog_screenshot("catalog_page")
        print(f"Скриншот создан: {screenshot_path}")
        
        # 4. Проверяем, что файл скриншота создан
        assert os.path.exists(screenshot_path), "Скриншот не создан"
        
        # 5. Проверяем, что файл не пустой
        file_size = os.path.getsize(screenshot_path)
        assert file_size > 0, "Файл скриншота пустой"
        print(f"Размер скриншота: {file_size} байт")
        
        print("[Тест] ПРОЙДЕН")


if __name__ == "__main__":
    pytest.main(["-v", __file__])