"""
Page Object для страницы логина Saucedemo
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from config.test_data import TestData


class LoginPage(BasePage):
    """Класс для работы со страницей логина"""
    
    # Локаторы элементов страницы
    USERNAME_INPUT = (By.XPATH, "//input[@id='user-name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@id='password']")
    LOGIN_BUTTON = (By.XPATH, "//input[@id='login-button']")
    ERROR_CONTAINER = (By.XPATH, "//div[@class='error-message-container error']")
    ERROR_TEXT = (By.XPATH, "//div[@class='error-message-container error']//h3")
    ERROR_CLOSE_BUTTON = (By.XPATH, "//button[@class='error-button']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open(self) -> None:
        """Открытие страницы логина"""
        self.driver.get(TestData.BASE_URL)
    
    def enter_username(self, username: str) -> None:
        """Ввод логина"""
        self.enter_text(self.USERNAME_INPUT, username)
    
    def enter_password(self, password: str) -> None:
        """Ввод пароля"""
        self.enter_text(self.PASSWORD_INPUT, password)
    
    def click_login_button(self) -> None:
        """Нажатие кнопки входа"""
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, username: str, password: str) -> None:
        """Выполнение авторизации"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def is_error_displayed(self) -> bool:
        """Проверка отображения сообщения об ошибке"""
        return self.is_element_displayed(self.ERROR_CONTAINER)
    
    def get_error_text(self) -> str:
        """Получение текста сообщения об ошибке"""
        return self.get_text(self.ERROR_TEXT)
    
    def close_error(self) -> None:
        """Закрытие сообщения об ошибке"""
        if self.is_error_displayed():
            self.click_element(self.ERROR_CLOSE_BUTTON)
    
    def is_error_closed(self) -> bool:
        """Проверка, что сообщение об ошибке закрыто"""
        return not self.is_error_displayed()
    
    def wait_for_error(self, timeout: int = 5) -> None:
        """Ожидание появления ошибки"""
        self.wait_for_element_visible(self.ERROR_CONTAINER, timeout)
    
    def clear_username_field(self) -> None:
        """Очистка поля логина"""
        element = self.find_element(self.USERNAME_INPUT)
        element.clear()
    
    def clear_password_field(self) -> None:
        """Очистка поля пароля"""
        element = self.find_element(self.PASSWORD_INPUT)
        element.clear()
    
    def select_all_in_username(self) -> None:
        """Выделение текста в поле логина"""
        element = self.find_element(self.USERNAME_INPUT)
        element.click()
        element.send_keys(Keys.CONTROL, "a")
    
    def select_all_in_password(self) -> None:
        """Выделение текста в поле пароля"""
        element = self.find_element(self.PASSWORD_INPUT)
        element.click()
        element.send_keys(Keys.CONTROL, "a")
    
    def press_tab(self) -> None:
        """Нажатие клавиши Tab"""
        self.driver.switch_to.active_element.send_keys(Keys.TAB)
    
    def press_enter(self) -> None:
        """Нажатие клавиши Enter"""
        self.driver.switch_to.active_element.send_keys(Keys.ENTER)
    
    def login_with_enter(self, username: str, password: str) -> None:
        """Авторизация через Enter"""
        self.enter_username(username)
        self.press_tab()
        self.enter_password(password)
        self.press_enter()
    
    def get_username_value(self) -> str:
        """Получение значения поля логина"""
        element = self.find_element(self.USERNAME_INPUT)
        return element.get_attribute("value")
    
    def get_password_value(self) -> str:
        """Получение значения поля пароля"""
        element = self.find_element(self.PASSWORD_INPUT)
        return element.get_attribute("value")
    
    def is_username_empty(self) -> bool:
        """Проверка, что поле логина пустое"""
        return self.get_username_value() == ""
    
    def is_password_empty(self) -> bool:
        """Проверка, что поле пароля пустое"""
        return self.get_password_value() == ""
    
    def take_catalog_screenshot(self, name: str = "catalog_page") -> str:
        """
        Создание скриншота страницы каталога
        
        Args:
            name: Имя файла для скриншота (по умолчанию "catalog_page")
        
        Returns:
            str: Путь к сохраненному скриншоту
        """
        from utils.helpers import take_screenshot
        return take_screenshot(self.driver, name)
    
    # =========================================================
    # МЕТОДЫ ДЛЯ РАБОТЫ С КАТАЛОГОМ ТОВАРОВ
    # =========================================================
    
    def get_all_add_to_cart_buttons(self) -> list:
        """
        Получение всех кнопок "Add to cart" на странице каталога
        
        Returns:
            list: Список элементов кнопок добавления в корзину
        """
        buttons = self.driver.find_elements(By.XPATH, "//button[contains(@id, 'add-to-cart')]")
        print(f"[INFO] Найдено кнопок 'Add to cart': {len(buttons)}")
        return buttons
    
    def add_all_items_to_cart(self) -> None:
        """
        Добавление всех товаров в корзину
        """
        print("[INFO] Начинаем добавление всех товаров в корзину...")
        buttons = self.get_all_add_to_cart_buttons()
        
        for i, button in enumerate(buttons, 1):
            button.click()
            print(f"[INFO] Товар {i} добавлен в корзину")
        
        print(f"[INFO] Все {len(buttons)} товаров добавлены в корзину")
    
    def go_to_cart(self) -> None:
        """
        Переход в корзину
        """
        cart_icon = self.driver.find_element(By.XPATH, "//div[@id='shopping_cart_container']/a")
        cart_icon.click()
        print("[INFO] Переход в корзину выполнен")
    
    def get_cart_items(self) -> list:
        """
        Получение всех элементов в корзине
        
        Returns:
            list: Список элементов товаров в корзине
        """
        items = self.driver.find_elements(By.XPATH, "//div[@class='cart_item']")
        print(f"[INFO] В корзине {len(items)} товаров")
        return items
    
    def scroll_to_last_cart_item(self) -> None:
        """
        Скроллинг страницы до последнего элемента в корзине
        Используется прокрутка с помощью JavaScript
        """
        print("[INFO] Скроллинг до последнего элемента в корзине...")
        
        cart_items = self.get_cart_items()
        
        if len(cart_items) == 0:
            print("[INFO] Корзина пуста, скроллинг не требуется")
            return
        
        last_item = cart_items[-1]
        
        # Прокрутка с помощью JavaScript (работает всегда)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", last_item)
        print(f"[INFO] Выполнен скроллинг до последнего элемента корзины (элемент {len(cart_items)})")
        
        import time
        time.sleep(0.5)
    
    def scroll_to_element_js(self, element) -> None:
        """
        Скроллинг страницы до указанного элемента с помощью JavaScript
        
        Args:
            element: Веб-элемент, до которого нужно прокрутить страницу
        """
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        print("[INFO] Выполнен скроллинг до указанного элемента")
    
    def get_cart_item_count(self) -> int:
        """
        Получение количества товаров в корзине
        
        Returns:
            int: Количество товаров в корзине
        """
        cart_badge = self.driver.find_elements(By.XPATH, "//span[@class='shopping_cart_badge']")
        if cart_badge:
            count = int(cart_badge[0].text)
            print(f"[INFO] В корзине товаров: {count}")
            return count
        print("[INFO] Корзина пуста")
        return 0