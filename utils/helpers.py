"""
Вспомогательные функции для тестов
"""

import time
import os
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver


def wait(seconds: int = 1) -> None:
    """Задержка выполнения кода"""
    time.sleep(seconds)


def get_current_datetime() -> str:
    """Получение текущей даты и времени в формате для имен файлов"""
    now = datetime.now()
    formatted = now.strftime("%Y-%m-%d_%H-%M-%S")
    return formatted


def take_screenshot(driver: WebDriver, name: str = None) -> str:
    """Создание скриншота страницы с автоматическим именем по дате/времени"""
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
        print("[INFO] Создана папка для скриншотов: screenshots")
    
    timestamp = get_current_datetime()
    
    if name:
        filename = f"{name}_{timestamp}.png"
    else:
        filename = f"{timestamp}.png"
    
    filepath = os.path.join("screenshots", filename)
    driver.save_screenshot(filepath)
    print(f"[INFO] Скриншот сохранен: {filepath}")
    
    return filepath


def take_screenshot_with_date(driver: WebDriver, prefix: str = "screenshot") -> str:
    """Создание скриншота с датой в имени файла"""
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{prefix}_{current_date}.png"
    filepath = os.path.join("screenshots", filename)
    
    driver.save_screenshot(filepath)
    print(f"[INFO] Скриншот с датой сохранен: {filepath}")
    
    return filepath