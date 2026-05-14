"""
Тестовые данные для авторизации на сайте Saucedemo
"""


class TestData:
    """Класс с тестовыми данными"""
    
    # URL
    BASE_URL = "https://www.saucedemo.com/"
    
    # Позитивные тестовые данные
    VALID_USERNAME = "standard_user"
    VALID_PASSWORD = "secret_sauce"
    
    # Негативные тестовые данные
    INVALID_USERNAME = "wrong_user"
    INVALID_PASSWORD = "wrong_password"
    LOCKED_USERNAME = "locked_out_user"
    
    # Ожидаемые тексты ошибок
    ERROR_MATCH = "Epic sadface: Username and password do not match any user in this service"
    ERROR_REQUIRED = "Epic sadface: Username is required"
    ERROR_LOCKED = "Epic sadface: Sorry, this user has been locked out."
    
    # Ожидаемый URL после успешной авторизации
    SUCCESS_URL_PART = "inventory.html"