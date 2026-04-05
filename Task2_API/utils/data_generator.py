import random
import string
from faker import Faker
from config import config

fake = Faker()
Faker.seed(42)  

class DataGenerator:
    """Генератор тестовых данных"""
    
    @staticmethod
    def generate_seller_id() -> int:
        """Генерация валидного sellerId"""
        return random.randint(config.SELLER_ID_MIN, config.SELLER_ID_MAX)
    
    @staticmethod
    def generate_name(length: int = None) -> str:
        """Генерация имени объявления"""
        if length:
            return ''.join(random.choices(string.ascii_letters, k=length))
        return fake.catch_phrase()
    
    @staticmethod
    def generate_price(min_price: int = 0, max_price: int = 1000000) -> int:
        """Генерация цены"""
        return random.randint(min_price, max_price)
    
    @staticmethod
    def generate_statistics() -> dict:
        """Генерация статистики"""
        return {
            "contacts": random.randint(0, 10000),
            "likes": random.randint(0, 10000),
            "viewCount": random.randint(0, 100000)
        }
    
    @staticmethod
    def generate_valid_item(seller_id: int = None) -> dict:
        """Генерация валидного объявления"""
        return {
            "sellerId": seller_id or DataGenerator.generate_seller_id(),
            "name": DataGenerator.generate_name(),
            "price": DataGenerator.generate_price(),
            "statistics": DataGenerator.generate_statistics()
        }
    
    @staticmethod
    def generate_item_without_field(field: str) -> dict:
        """Генерация объявления без указанного поля"""
        item = DataGenerator.generate_valid_item()
        if field in item:
            del item[field]
        return item
    
    @staticmethod
    def generate_item_with_null_field(field: str) -> dict:
        """Генерация объявления с null в указанном поле"""
        item = DataGenerator.generate_valid_item()
        item[field] = None
        return item

data_generator = DataGenerator()