"""
Page Object для страницы логина Saucedemo
"""

import time
from typing import Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from config.test_data import TestData


class LoginPage(BasePage):
    """Класс для работы со страницей логина"""
    
    # Локаторы элементов страницы
    USERNAME_INPUT: Tuple[str, str] = (By.XPATH, "//input[@id='user-name']")
    PASSWORD_INPUT: Tuple[str, str] = (By.XPATH, "//input[@id='password']")
    LOGIN_BUTTON: Tuple[str, str] = (By.XPATH, "//input[@id='login-button']")
    ERROR_CONTAINER: Tuple[str, str] = (By.XPATH, "//div[@class='error-message-container error']")
    ERROR_TEXT: Tuple[str, str] = (By.XPATH, "//div[@class='error-message-container error']//h3")
    ERROR_CLOSE_BUTTON: Tuple[str, str] = (By.XPATH, "//button[@class='error-button']")
    
    # Локаторы для бургер-меню и выхода
    BURGER_MENU_BUTTON: Tuple[str, str] = (By.XPATH, "//button[@id='react-burger-menu-btn']")
    LOGOUT_BUTTON: Tuple[str, str] = (By.XPATH, "//a[@id='logout_sidebar_link']")
    
    def __init__(self, driver) -> None:
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
        """Нажатие кнопки входа через JavaScript (надежно)"""
        button = self.find_element(self.LOGIN_BUTTON)
        self.driver.execute_script("arguments[0].click();", button)
        print("[INFO] Кнопка Login нажата через JavaScript")
    
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
    
    # =========================================================
    # МЕТОДЫ ДЛЯ ИМИТАЦИИ НАЖАТИЯ КЛАВИШ
    # =========================================================
    
    def select_all_in_username(self) -> None:
        """Выделение всего текста в поле логина (Ctrl+A)"""
        element = self.find_element(self.USERNAME_INPUT)
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        print("[INFO] Текст в поле логина выделен (Ctrl+A)")
    
    def select_all_in_password(self) -> None:
        """Выделение всего текста в поле пароля (Ctrl+A)"""
        element = self.find_element(self.PASSWORD_INPUT)
        element.click()
        element.send_keys(Keys.CONTROL, "a")
        print("[INFO] Текст в поле пароля выделен (Ctrl+A)")
    
    def delete_selected_username(self) -> None:
        """Удаление выделенного текста в поле логина (DELETE)"""
        element = self.find_element(self.USERNAME_INPUT)
        element.click()
        element.send_keys(Keys.DELETE)
        print("[INFO] Текст в поле логина удален (DELETE)")
    
    def delete_selected_password(self) -> None:
        """Удаление выделенного текста в поле пароля (DELETE)"""
        element = self.find_element(self.PASSWORD_INPUT)
        element.click()
        element.send_keys(Keys.DELETE)
        print("[INFO] Текст в поле пароля удален (DELETE)")
    
    def clear_username_with_keys(self) -> None:
        """Очистка поля логина через JavaScript (гарантированно)"""
        element = self.find_element(self.USERNAME_INPUT)
        self.driver.execute_script("arguments[0].value = '';", element)
        print("[INFO] Поле логина очищено через JavaScript")
    
    def clear_password_with_keys(self) -> None:
        """Очистка поля пароля через JavaScript (гарантированно)"""
        element = self.find_element(self.PASSWORD_INPUT)
        self.driver.execute_script("arguments[0].value = '';", element)
        print("[INFO] Поле пароля очищено через JavaScript")
    
    def clear_all_fields_with_keys(self) -> None:
        """Очистка всех полей ввода через JavaScript"""
        print("[INFO] Очистка полей через JavaScript...")
        self.clear_username_with_keys()
        self.clear_password_with_keys()
        print("[INFO] Все поля очищены")
    
    def type_username_with_keys(self, username: str) -> None:
        """Ввод логина с помощью клавиатуры"""
        element = self.find_element(self.USERNAME_INPUT)
        element.click()
        element.send_keys(username)
        print(f"[INFO] Логин '{username}' введен")
    
    def type_password_with_keys(self, password: str) -> None:
        """Ввод пароля с помощью клавиатуры"""
        element = self.find_element(self.PASSWORD_INPUT)
        element.click()
        element.send_keys(password)
        print("[INFO] Пароль введен")
    
    def press_tab(self) -> None:
        """Нажатие клавиши Tab через JavaScript"""
        self.driver.execute_script("""
            var element = document.activeElement;
            if(element) {
                var event = new KeyboardEvent('keydown', {key: 'Tab', bubbles: true});
                element.dispatchEvent(event);
            }
        """)
        print("[INFO] Нажата клавиша TAB")
    
    def login_with_keys(self, username: str, password: str) -> None:
        """Авторизация с использованием клавиатуры (полный способ)"""
        print("\n[INFO] Начинаем процесс авторизации...")
        
        self.clear_username_with_keys()
        self.type_username_with_keys(username)
        self.press_tab()
        self.clear_password_with_keys()
        self.type_password_with_keys(password)
        self.click_login_button()
        
        print("[INFO] Авторизация выполнена")
    
    def get_username_value(self) -> str:
        """Получение значения поля логина"""
        return self.get_element_value(self.USERNAME_INPUT)
    
    def get_password_value(self) -> str:
        """Получение значения поля пароля"""
        return self.get_element_value(self.PASSWORD_INPUT)
    
    def is_username_empty(self) -> bool:
        """Проверка, что поле логина пустое"""
        return self.get_username_value() == ""
    
    def is_password_empty(self) -> bool:
        """Проверка, что поле пароля пустое"""
        return self.get_password_value() == ""
    
    # =========================================================
    # МЕТОДЫ ДЛЯ РАБОТЫ С МЕНЮ И ВЫХОДОМ ИЗ СИСТЕМЫ
    # =========================================================
    
    def open_burger_menu(self) -> None:
        """
        Открытие скрытого бургер-меню
        Нажатие на иконку с тремя горизонтальными полосками в левом верхнем углу
        """
        burger_menu = self.find_element(self.BURGER_MENU_BUTTON)
        burger_menu.click()
        print("[INFO] Бургер-меню открыто")
    
    def click_logout(self) -> None:
        """
        Нажатие на кнопку Logout в скрытом меню
        Выполняется после открытия бургер-меню
        """
        logout_button = self.find_element(self.LOGOUT_BUTTON)
        logout_button.click()
        print("[INFO] Кнопка Logout нажата, выполнен выход из системы")
    
    def logout(self) -> None:
        """
        Полный процесс выхода из системы:
        1. Открыть бургер-меню
        2. Нажать кнопку Logout
        """
        print("[INFO] Начинаем процесс выхода из системы...")
        self.open_burger_menu()
        self.click_logout()
        print("[INFO] Выход из системы выполнен")
    
    def is_logged_in(self) -> bool:
        """
        Проверка, что пользователь авторизован
        (находится на странице инвентаря)
        
        Returns:
            bool: True если авторизован, иначе False
        """
        return "inventory.html" in self.driver.current_url
    
    def is_logged_out(self) -> bool:
        """
        Проверка, что пользователь вышел из системы
        (находится на странице логина)
        
        Returns:
            bool: True если не авторизован, иначе False
        """
        current_url = self.driver.current_url
        return current_url == TestData.BASE_URL or "saucedemo.com" in current_url and "inventory" not in current_url
    
    # =========================================================
    # МЕТОДЫ ДЛЯ РАБОТЫ С ТОВАРАМИ И КОРЗИНОЙ
    # =========================================================
    
    def get_item_name_by_index(self, index: int) -> str:
        """
        Получение названия товара по индексу в списке товаров
        
        Args:
            index: Индекс товара (начинается с 0)
        
        Returns:
            str: Название товара
        """
        item_name = self.driver.find_element(By.XPATH, f"(//div[@class='inventory_item_name'])[{index + 1}]")
        name = item_name.text
        print(f"[INFO] Товар {index + 1}: название - '{name}'")
        return name
    
    def get_item_price_by_index(self, index: int) -> float:
        """
        Получение цены товара по индексу в списке товаров
        
        Args:
            index: Индекс товара (начинается с 0)
        
        Returns:
            float: Цена товара в виде числа
        """
        item_price = self.driver.find_element(By.XPATH, f"(//div[@class='inventory_item_price'])[{index + 1}]")
        price_text = item_price.text.replace("$", "")
        price = float(price_text)
        print(f"[INFO] Товар {index + 1}: цена - ${price}")
        return price
    
    def add_item_to_cart_by_index(self, index: int) -> None:
        """
        Добавление товара в корзину по индексу
        
        Args:
            index: Индекс товара (начинается с 0)
        """
        add_button = self.driver.find_element(By.XPATH, f"(//button[contains(@id, 'add-to-cart')])[{index + 1}]")
        add_button.click()
        print(f"[INFO] Товар {index + 1} добавлен в корзину")
    
    def get_all_add_to_cart_buttons(self) -> list:
        """Получение всех кнопок добавления в корзину"""
        buttons = self.driver.find_elements(By.XPATH, "//button[contains(@id, 'add-to-cart')]")
        print(f"[INFO] Найдено кнопок 'Add to cart': {len(buttons)}")
        return buttons
    
    def add_all_items_to_cart(self) -> None:
        """Добавление всех товаров в корзину"""
        print("[INFO] Добавление всех товаров в корзину...")
        buttons = self.get_all_add_to_cart_buttons()
        for i, button in enumerate(buttons, 1):
            button.click()
            print(f"[INFO] Товар {i} добавлен в корзину")
        print(f"[INFO] Все {len(buttons)} товаров добавлены в корзину")
    
    def go_to_cart(self) -> None:
        """Переход в корзину"""
        cart_icon = self.driver.find_element(By.XPATH, "//div[@id='shopping_cart_container']/a")
        cart_icon.click()
        print("[INFO] Переход в корзину выполнен")
    
    def get_cart_items(self) -> list:
        """Получение всех элементов в корзине"""
        items = self.driver.find_elements(By.XPATH, "//div[@class='cart_item']")
        print(f"[INFO] В корзине {len(items)} товаров")
        return items
    
    def get_cart_item_name_by_index(self, index: int) -> str:
        """
        Получение названия товара в корзине по индексу
        
        Args:
            index: Индекс товара в корзине (начинается с 0)
        
        Returns:
            str: Название товара в корзине
        """
        item_name = self.driver.find_element(By.XPATH, f"(//div[@class='inventory_item_name'])[{index + 1}]")
        name = item_name.text
        print(f"[INFO] Товар в корзине {index + 1}: название - '{name}'")
        return name
    
    def get_cart_item_price_by_index(self, index: int) -> float:
        """
        Получение цены товара в корзине по индексу
        
        Args:
            index: Индекс товара в корзине (начинается с 0)
        
        Returns:
            float: Цена товара в корзине в виде числа
        """
        item_price = self.driver.find_element(By.XPATH, f"(//div[@class='inventory_item_price'])[{index + 1}]")
        price_text = item_price.text.replace("$", "")
        price = float(price_text)
        print(f"[INFO] Товар в корзине {index + 1}: цена - ${price}")
        return price
    
    def get_cart_item_count_in_cart(self) -> int:
        """
        Получение количества товаров в корзине
        
        Returns:
            int: Количество товаров
        """
        items = self.driver.find_elements(By.XPATH, "//div[@class='cart_item']")
        count = len(items)
        print(f"[INFO] В корзине {count} товаров")
        return count
    
    def scroll_to_last_cart_item(self) -> None:
        """Скроллинг до последнего элемента в корзине"""
        cart_items = self.get_cart_items()
        if len(cart_items) > 0:
            last_item = cart_items[-1]
            self.driver.execute_script("arguments[0].scrollIntoView(true);", last_item)
            print("[INFO] Скроллинг до последнего элемента выполнен")
    
    def get_cart_item_count(self) -> int:
        """Получение количества товаров в корзине (из бейджа)"""
        cart_badge = self.driver.find_elements(By.XPATH, "//span[@class='shopping_cart_badge']")
        if cart_badge:
            count = int(cart_badge[0].text)
            print(f"[INFO] В корзине товаров: {count}")
            return count
        return 0
    
    # =========================================================
    # МЕТОДЫ ДЛЯ ПРОЦЕССА ОФОРМЛЕНИЯ ЗАКАЗА (CHECKOUT)
    # =========================================================
    
    def click_checkout_button(self) -> None:
        """Нажатие кнопки Checkout"""
        checkout_button = self.driver.find_element(By.XPATH, "//button[@id='checkout']")
        checkout_button.click()
        print("[INFO] Нажата кнопка Checkout")
    
    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        """
        Заполнение информации о покупателе
        
        Args:
            first_name: Имя
            last_name: Фамилия
            postal_code: Почтовый индекс
        """
        first_name_field = self.driver.find_element(By.XPATH, "//input[@id='first-name']")
        last_name_field = self.driver.find_element(By.XPATH, "//input[@id='last-name']")
        postal_code_field = self.driver.find_element(By.XPATH, "//input[@id='postal-code']")
        
        first_name_field.send_keys(first_name)
        last_name_field.send_keys(last_name)
        postal_code_field.send_keys(postal_code)
        
        print(f"[INFO] Заполнены данные: {first_name} {last_name}, {postal_code}")
    
    def click_continue_button(self) -> None:
        """Нажатие кнопки Continue"""
        continue_button = self.driver.find_element(By.XPATH, "//input[@id='continue']")
        continue_button.click()
        print("[INFO] Нажата кнопка Continue")
    
    def click_finish_button(self) -> None:
        """Нажатие кнопки Finish"""
        finish_button = self.driver.find_element(By.XPATH, "//button[@id='finish']")
        finish_button.click()
        print("[INFO] Нажата кнопка Finish")
    
    def get_cart_total_sum(self) -> float:
        """
        Получение общей суммы товаров в корзине
        
        Returns:
            float: Общая сумма
        """
        total_element = self.driver.find_element(By.XPATH, "//div[@class='summary_subtotal_label']")
        total_text = total_element.text.replace("Item total: $", "")
        total = float(total_text)
        print(f"[INFO] Общая сумма товаров: ${total}")
        return total
    
    def get_complete_message(self) -> str:
        """
        Получение сообщения об успешном завершении покупки
        
        Returns:
            str: Текст сообщения
        """
        message = self.driver.find_element(By.XPATH, "//h2[@class='complete-header']")
        return message.text
    
    def take_catalog_screenshot(self, name: str = "catalog_page") -> str:
        """Создание скриншота страницы каталога"""
        from utils.helpers import take_screenshot
        return take_screenshot(self.driver, name)
    
    # =========================================================
    # МЕТОДЫ ДЛЯ НАВИГАЦИИ (BACK И FORWARD)
    # =========================================================
    
    def go_back(self) -> None:
        """
        Возврат на предыдущую страницу (назад)
        Используется метод driver.back() для имитации нажатия кнопки "Назад" в браузере
        """
        print(f"[INFO] Переход на предыдущую страницу. Текущий URL: {self.driver.current_url}")
        self.driver.back()
        time.sleep(1)
        print(f"[INFO] Переход выполнен. Текущий URL: {self.driver.current_url}")
    
    def go_forward(self) -> None:
        """
        Переход на следующую страницу (вперед)
        Используется метод driver.forward() для имитации нажатия кнопки "Вперед" в браузере
        """
        print(f"[INFO] Переход на следующую страницу. Текущий URL: {self.driver.current_url}")
        self.driver.forward()
        time.sleep(1)
        print(f"[INFO] Переход выполнен. Текущий URL: {self.driver.current_url}")
    
    def navigate_back_to_catalog(self) -> None:
        """
        Навигация назад на страницу каталога
        Возврат с любой страницы на предыдущую (страницу каталога)
        """
        print("[INFO] Возврат на страницу каталога (назад)...")
        self.go_back()
    
    def navigate_forward_to_cart(self) -> None:
        """
        Навигация вперед на страницу корзины
        Переход с предыдущей страницы на следующую (страницу корзины)
        """
        print("[INFO] Переход вперед на страницу корзины...")
        self.go_forward()
    # =========================================================
    # МЕТОДЫ ДЛЯ НАВИГАЦИИ (BACK И FORWARD)
    # =========================================================
    
    def go_back(self) -> None:
        """
        Возврат на предыдущую страницу (назад)
        Используется метод driver.back() для имитации нажатия кнопки "Назад" в браузере
        
        Returns:
            None
        """
        print(f"[INFO] Переход на предыдущую страницу. Текущий URL: {self.driver.current_url}")
        self.driver.back()
        import time
        time.sleep(1)
        print(f"[INFO] Переход выполнен. Текущий URL: {self.driver.current_url}")
    
    def go_forward(self) -> None:
        """
        Переход на следующую страницу (вперед)
        Используется метод driver.forward() для имитации нажатия кнопки "Вперед" в браузере
        
        Returns:
            None
        """
        print(f"[INFO] Переход на следующую страницу. Текущий URL: {self.driver.current_url}")
        self.driver.forward()
        import time
        time.sleep(1)
        print(f"[INFO] Переход выполнен. Текущий URL: {self.driver.current_url}")