import os

class Config:
    """Конфигурация тестового окружения"""
    
    # Базовый URL API
    BASE_URL = os.getenv("BASE_URL", "https://qa-internship.avito.com")
    
    # Версии API
    API_V1 = "/api/1"
    API_V2 = "/api/2"
    
    # Таймауты (в секундах)
    TIMEOUT = 30
    TIMEOUT_LONG = 60
    
    # Допустимый диапазон sellerId
    SELLER_ID_MIN = 111111
    SELLER_ID_MAX = 999999
    
    # Ограничения полей
    NAME_MAX_LENGTH = 1000
    PRICE_MAX = 10**12
    
    # Заголовки по умолчанию
    DEFAULT_HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Ретри при неудачных запросах
    RETRY_COUNT = 3
    RETRY_DELAY = 1

config = Config()