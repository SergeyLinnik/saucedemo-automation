"""
Фабрика для создания веб-драйверов
Использует локальные драйверы для стабильности
"""

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os


class DriverFactory:
    """Класс для создания и настройки веб-драйверов"""
    
    # Путь к локальному драйверу Firefox (GeckoDriver)
    # Если файл не найден, будет использован автоматический менеджер
    @staticmethod
    def get_driver(headless: bool = False) -> webdriver.Firefox:
        """
        Создание драйвера Firefox с использованием локального драйвера
        
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
        
        # Пробуем использовать локальный драйвер
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        driver_path = os.path.join(current_dir, "geckodriver.exe")
        
        if os.path.exists(driver_path):
            print(f"[INFO] Используется локальный драйвер: {driver_path}")
            service = Service(driver_path)
            driver = webdriver.Firefox(service=service, options=firefox_options)
        else:
            print("[INFO] Локальный драйвер не найден, используется webdriver-manager")
            from webdriver_manager.firefox import GeckoDriverManager
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