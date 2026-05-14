"""
Базовый класс Page Object
Содержит общие методы для всех страниц
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class BasePage:
    """Базовый класс для всех Page Object"""
    
    def __init__(self, driver):
        """
        Инициализация базовой страницы
        
        Args:
            driver: Экземпляр веб-драйвера
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator: tuple, timeout: int = 10) -> WebElement:
        """
        Поиск элемента с ожиданием
        
        Args:
            locator: Кортеж (By.XPATH, "xpath_expression")
            timeout: Время ожидания в секундах
        
        Returns:
            WebElement: Найденный элемент
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    def click_element(self, locator: tuple, timeout: int = 10) -> None:
        """
        Клик по элементу с ожиданием
        
        Args:
            locator: Кортеж (By.XPATH, "xpath_expression")
            timeout: Время ожидания в секундах
        """
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator: tuple, text: str, timeout: int = 10) -> None:
        """
        Ввод текста в поле
        
        Args:
            locator: Кортеж (By.XPATH, "xpath_expression")
            text: Текст для ввода
            timeout: Время ожидания в секундах
        """
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator: tuple, timeout: int = 10) -> str:
        """
        Получение текста элемента
        
        Args:
            locator: Кортеж (By.XPATH, "xpath_expression")
            timeout: Время ожидания в секундах
        
        Returns:
            str: Текст элемента
        """
        element = self.find_element(locator, timeout)
        return element.text
    
    def is_element_displayed(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Проверка отображения элемента
        
        Args:
            locator: Кортеж (By.XPATH, "xpath_expression")
            timeout: Время ожидания в секундах
        
        Returns:
            bool: True если элемент отображается, иначе False
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False
    
    def get_current_url(self) -> str:
        """
        Получение текущего URL
        
        Returns:
            str: Текущий URL страницы
        """
        return self.driver.current_url
    
    def wait_for_url_contains(self, text: str, timeout: int = 10) -> bool:
        """
        Ожидание, что URL содержит указанный текст
        
        Args:
            text: Ожидаемый текст в URL
            timeout: Время ожидания в секундах
        
        Returns:
            bool: True если URL содержит текст
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.url_contains(text))
    
    def wait_for_element_visible(self, locator: tuple, timeout: int = 10) -> WebElement:
        """
        Ожидание видимости элемента
        
        Args:
            locator: Кортеж (By.XPATH, "xpath_expression")
            timeout: Время ожидания в секундах
        
        Returns:
            WebElement: Видимый элемент
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def refresh_page(self, wait_seconds: int = 2) -> None:
        """
        Обновление текущей страницы (перезагрузка)
        
        Args:
            wait_seconds: Время ожидания после обновления в секундах
        """
        print(f"[INFO] Обновление страницы. Текущий URL: {self.get_current_url()}")
        self.driver.refresh()
        self.delay(wait_seconds)
        print(f"[INFO] Страница обновлена. Новый URL: {self.get_current_url()}")
    
    def delay(self, seconds: int) -> None:
        """
        Функция задержки выполнения кода на определенное количество секунд
        
        Args:
            seconds: Количество секунд для задержки
        """
        print(f"[INFO] Задержка на {seconds} секунд...")
        time.sleep(seconds)
        print(f"[INFO] Задержка завершена")
    
    def refresh_with_retry(self, max_retries: int = 3, delay_between: int = 2) -> bool:
        """
        Обновление страницы с повторными попытками при ошибке
        
        Args:
            max_retries: Максимальное количество попыток обновления
            delay_between: Задержка между попытками в секундах
        
        Returns:
            bool: True если обновление успешно, False если все попытки не удались
        """
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