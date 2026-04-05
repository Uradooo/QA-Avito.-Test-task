import requests
import time
from typing import Dict, Any, Optional
from config import config

class APIClient:
    """Клиент для работы с API объявлений"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or config.BASE_URL
        self.session = requests.Session()
        self.session.headers.update(config.DEFAULT_HEADERS)
    
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Выполнение HTTP-запроса с повторными попытками"""
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(config.RETRY_COUNT):
            try:
                response = self.session.request(method, url, timeout=config.TIMEOUT, **kwargs)
                return response
            except requests.RequestException as e:
                if attempt == config.RETRY_COUNT - 1:
                    raise
                time.sleep(config.RETRY_DELAY)
    
    def create_item(self, item_data: Dict[str, Any]) -> requests.Response:
        """Создание объявления"""
        return self._request("POST", f"{config.API_V1}/item", json=item_data)
    
    def get_item(self, item_id: str) -> requests.Response:
        """Получение объявления по ID"""
        return self._request("GET", f"{config.API_V1}/item/{item_id}")
    
    def get_seller_items(self, seller_id: int) -> requests.Response:
        """Получение всех объявлений продавца"""
        return self._request("GET", f"{config.API_V1}/{seller_id}/item")
    
    def get_statistic(self, item_id: str) -> requests.Response:
        """Получение статистики по объявлению"""
        return self._request("GET", f"{config.API_V1}/statistic/{item_id}")
    
    def delete_item(self, item_id: str) -> requests.Response:
        """Удаление объявления"""
        return self._request("DELETE", f"{config.API_V2}/item/{item_id}")
    
    def extract_item_id(self, response: requests.Response) -> str:
        """Извлечение ID объявления из ответа"""
        # Формат: "Сохранили объявление - 123456789"
        if response.status_code == 200:
            status_text = response.json().get("status", "")
            if " - " in status_text:
                return status_text.split(" - ")[1]
        return None

api_client = APIClient()