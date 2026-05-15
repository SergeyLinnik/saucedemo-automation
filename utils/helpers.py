"""
Вспомогательные функции для тестов
"""

import time
from typing import Union


def wait(seconds: Union[int, float] = 1) -> None:
    """
    Функция задержки выполнения кода на определенное количество секунд
    
    Args:
        seconds: Количество секунд для задержки (может быть int или float)
    
    Примеры:
        wait(1)     # Пауза на 1 секунду
        wait(2.5)   # Пауза на 2.5 секунды
        wait(0.5)   # Пауза на 0.5 секунды
    """
    print(f"[INFO] Задержка на {seconds} секунд...")
    time.sleep(seconds)
    print("[INFO] Задержка завершена")


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


# =========================================================
# НОВЫЕ ФУНКЦИИ (ДОБАВЛЯЕМ ИХ В КОНЕЦ ФАЙЛА)
# =========================================================

def wait_short() -> None:
    """
    Короткая задержка (1 секунда)
    Используется для быстрых пауз между действиями
    """
    wait(1)


def wait_medium() -> None:
    """
    Средняя задержка (3 секунды)
    Используется для ожидания загрузки элементов
    """
    wait(3)


def wait_long() -> None:
    """
    Длинная задержка (5 секунд)
    Используется для ожидания анимаций или медленных операций
    """
    wait(5)


def refresh_page(driver) -> None:
    """
    Обновление текущей страницы
    
    Args:
        driver: Экземпляр веб-драйвера
    """
    print(f"[INFO] Обновление страницы. Текущий URL: {driver.current_url}")
    driver.refresh()
    wait(2)
    print(f"[INFO] Страница обновлена. Новый URL: {driver.current_url}")


def safe_refresh(driver, max_attempts: int = 3) -> bool:
    """
    Безопасное обновление страницы с повторными попытками
    
    Args:
        driver: Экземпляр веб-драйвера
        max_attempts: Максимальное количество попыток
    
    Returns:
        bool: True если обновление успешно
    """
    for attempt in range(max_attempts):
        try:
            print(f"[INFO] Попытка обновления {attempt + 1} из {max_attempts}")
            driver.refresh()
            wait(2)
            return True
        except Exception as error:
            print(f"[WARN] Ошибка при обновлении: {error}")
            wait(2)
    
    print(f"[ERROR] Не удалось обновить страницу после {max_attempts} попыток")
    return False