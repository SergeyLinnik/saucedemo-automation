"""
Вспомогательные функции для тестов
"""

import time


def wait(seconds: int = 1) -> None:
    """
    Ожидание указанное количество секунд
    
    Args:
        seconds: Количество секунд для ожидания
    """
    time.sleep(seconds)


def is_url_contains(driver, expected_part: str) -> bool:
    """
    Проверка, что URL содержит ожидаемую часть
    
    Args:
        driver: Экземпляр веб-драйвера
        expected_part: Ожидаемая часть URL
    
    Returns:
        bool: True если URL содержит часть, иначе False
    """
    return expected_part in driver.current_url