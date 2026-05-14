"""
Фабрика для создания веб-драйверов
"""

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager


class DriverFactory:
    """Класс для создания и настройки веб-драйверов"""
    
    @staticmethod
    def get_driver(headless: bool = False) -> webdriver.Firefox:
        """
        Создание драйвера Firefox
        
        Args:
            headless: Запускать ли браузер в headless режиме
        
        Returns:
            webdriver.Firefox: Настроенный экземпляр драйвера
        """
        firefox_options = FirefoxOptions()
        
        if headless:
            firefox_options.add_argument("--headless")
            firefox_options.add_argument("--window-size=1920,1080")
        
        firefox_options.add_argument("--start-maximized")
        
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=firefox_options)
        
        return driver
    
    @staticmethod
    def quit_driver(driver: webdriver.Firefox) -> None:
        """
        Закрытие драйвера
        
        Args:
            driver: Экземпляр веб-драйвера
        """
        if driver:
            driver.quit()