"""
Тест проверки метода обновления страницы
"""

import pytest
from pages.login_page import LoginPage
from config.test_data import TestData


class TestRefreshPage:
    """
    Класс с тестами для проверки обновления страницы
    """
    
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        """
        Настройка перед каждым тестом
        """
        self.login_page = LoginPage(driver)
        self.login_page.open()
    
    def test_refresh_before_login(self, driver):
        """
        Тест: Обновление страницы до входа
        """
        print("\n[Тест] Обновление страницы до входа")
        
        # Получаем текущий URL до обновления
        url_before = self.login_page.get_current_url()
        print(f"URL до обновления: {url_before}")
        
        # Обновляем страницу
        self.login_page.refresh_page(wait_seconds=2)
        
        # Проверяем, что URL не изменился (мы на той же странице)
        url_after = self.login_page.get_current_url()
        print(f"URL после обновления: {url_after}")
        
        assert url_before == url_after, "URL изменился после обновления"
        print("Успех: URL не изменился после обновления")
        
        # Проверяем, что поле логина все еще доступно
        assert self.login_page.is_element_displayed(self.login_page.USERNAME_INPUT), \
            "Поле логина не отображается после обновления"
        print("Успех: Поле логина отображается после обновления")
        
        print("[Тест] ПРОЙДЕН")
    
    def test_refresh_with_delay(self, driver):
        """
        Тест: Обновление страницы с пользовательской задержкой
        """
        print("\n[Тест] Обновление страницы с задержкой 5 секунд")
        
        import time
        start_time = time.time()
        
        # Обновляем страницу с задержкой 5 секунд
        self.login_page.refresh_page(wait_seconds=5)
        
        end_time = time.time()
        elapsed = end_time - start_time
        
        print(f"Прошло времени: {elapsed:.2f} секунд")
        assert elapsed >= 5, f"Задержка была меньше 5 секунд: {elapsed:.2f}"
        
        print("[Тест] ПРОЙДЕН")
    
    def test_refresh_after_failed_login(self, driver):
        """
        Тест: Обновление страницы после неудачной авторизации
        """
        print("\n[Тест] Обновление страницы после неудачной авторизации")
        
        # Выполняем неудачную авторизацию
        self.login_page.login(TestData.VALID_USERNAME, TestData.INVALID_PASSWORD)
        
        # Проверяем, что ошибка отображается
        assert self.login_page.is_error_displayed(), "Ошибка не отображается"
        print("Ошибка отображается до обновления")
        
        # Обновляем страницу
        self.login_page.refresh_page(wait_seconds=2)
        
        # Проверяем, что ошибка исчезла после обновления
        assert not self.login_page.is_error_displayed(), \
            "Ошибка все еще отображается после обновления"
        print("Успех: Ошибка исчезла после обновления")
        
        # Проверяем, что поля ввода пустые
        username_field = self.login_page.find_element(self.login_page.USERNAME_INPUT)
        password_field = self.login_page.find_element(self.login_page.PASSWORD_INPUT)
        
        assert username_field.get_attribute("value") == "", "Поле логина не пустое"
        assert password_field.get_attribute("value") == "", "Поле пароля не пустое"
        print("Успех: Поля ввода очищены после обновления")
        
        print("[Тест] ПРОЙДЕН")
    
    def test_delay_function(self, driver):
        """
        Тест: Проверка функции задержки
        """
        print("\n[Тест] Проверка функции задержки")
        
        import time
        
        # Тест задержки на 2 секунды
        start_time = time.time()
        self.login_page.delay(2)
        end_time = time.time()
        elapsed = end_time - start_time
        
        assert elapsed >= 2, f"Задержка была меньше 2 секунд: {elapsed:.2f}"
        print(f"Задержка на 2 секунды отработала: {elapsed:.2f} сек")
        
        # Тест задержки на 0.5 секунды
        start_time = time.time()
        self.login_page.delay(1)
        end_time = time.time()
        elapsed = end_time - start_time
        
        assert elapsed >= 1, f"Задержка была меньше 1 секунды: {elapsed:.2f}"
        print(f"Задержка на 1 секунду отработала: {elapsed:.2f} сек")
        
        print("[Тест] ПРОЙДЕН")
    
    def test_refresh_with_retry(self, driver):
        """
        Тест: Обновление страницы с повторными попытками
        """
        print("\n[Тест] Обновление страницы с повторными попытками")
        
        # Обновляем страницу с повторными попытками
        result = self.login_page.refresh_with_retry(max_retries=3, delay_between=1)
        
        assert result, "Обновление страницы не удалось"
        print("Страница успешно обновлена с повторными попытками")
        
        # Проверяем, что страница загрузилась
        url = self.login_page.get_current_url()
        assert "saucedemo" in url, "Страница не загрузилась"
        print(f"Текущий URL: {url}")
        
        print("[Тест] ПРОЙДЕН")


if __name__ == "__main__":
    pytest.main(["-v", __file__])