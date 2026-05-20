"""
Базовый класс Page Object
Содержит общие методы для всех страниц
"""

from typing import Tuple
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class BasePage:
    """Базовый класс для всех Page Object"""
    
    def __init__(self, driver) -> None:
        """
        Инициализация базовой страницы
        
        Args:
            driver: Экземпляр веб-драйвера
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator: Tuple[str, str], timeout: int = 10) -> WebElement:
        """Поиск элемента с ожиданием"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    def click_element(self, locator: Tuple[str, str], timeout: int = 10) -> None:
        """Клик по элементу с ожиданием"""
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator: Tuple[str, str], text: str, timeout: int = 10) -> None:
        """Ввод текста в поле"""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator: Tuple[str, str], timeout: int = 10) -> str:
        """Получение текста элемента"""
        element = self.find_element(locator, timeout)
        return element.text
    
    def is_element_displayed(self, locator: Tuple[str, str], timeout: int = 5) -> bool:
        """Проверка отображения элемента"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False
    
    def get_current_url(self) -> str:
        """Получение текущего URL"""
        return self.driver.current_url
    
    def wait_for_url_contains(self, text: str, timeout: int = 10) -> bool:
        """Ожидание, что URL содержит указанный текст"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.url_contains(text))
    
    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: int = 10) -> WebElement:
        """Ожидание видимости элемента"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def refresh_page(self, wait_seconds: int = 2) -> None:
        """Обновление текущей страницы"""
        print(f"[INFO] Обновление страницы. Текущий URL: {self.get_current_url()}")
        self.driver.refresh()
        self.delay(wait_seconds)
        print(f"[INFO] Страница обновлена. Новый URL: {self.get_current_url()}")
    
    def delay(self, seconds: int) -> None:
        """Задержка выполнения кода"""
        print(f"[INFO] Задержка на {seconds} секунд...")
        time.sleep(seconds)
        print(f"[INFO] Задержка завершена")
    
    def refresh_with_retry(self, max_retries: int = 3, delay_between: int = 2) -> bool:
        """Обновление страницы с повторными попытками"""
        for attempt in range(max_retries):
            try:
                print(f"[INFO] Попытка обновления {attempt + 1} из {max_retries}")
                self.driver.refresh()
                self.delay(delay_between)
                current_url = self.get_current_url()
                if current_url and "saucedemo" in current_url:
                    print(f"[INFO] Страница успешно обновлена. URL: {current_url}")
                    return True
            except Exception as error:
                print(f"[WARN] Ошибка при обновлении: {error}")
                self.delay(delay_between)
        print(f"[ERROR] Не удалось обновить страницу после {max_retries} попыток")
        return False
    
    def clear_field(self, locator: Tuple[str, str]) -> None:
        """Очистка поля"""
        element = self.find_element(locator)
        element.clear()
    
    def get_element_value(self, locator: Tuple[str, str]) -> str:
        """Получение значения поля"""
        element = self.find_element(locator)
        return element.get_attribute("value")