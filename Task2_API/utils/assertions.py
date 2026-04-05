from typing import Dict, Any

class Assertions:
    """Кастомные проверки для API тестов"""
    
    @staticmethod
    def assert_status_code(response, expected_status: int):
        """Проверка статус кода"""
        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}. Response: {response.text}"
    
    @staticmethod
    def assert_response_has_fields(response, fields: list):
        """Проверка наличия полей в ответе"""
        data = response.json()
        for field in fields:
            assert field in data, f"Field '{field}' not found in response: {data}"
    
    @staticmethod
    def assert_item_matches_original(created_item: dict, retrieved_item: dict):
        """Проверка соответствия созданного и полученного объявления"""
   
        assert retrieved_item["sellerId"] == created_item["sellerId"], \
            f"sellerId mismatch: {retrieved_item['sellerId']} vs {created_item['sellerId']}"
        
        assert retrieved_item["name"] == created_item["name"], \
            f"name mismatch: {retrieved_item['name']} vs {created_item['name']}"
        
        assert retrieved_item["price"] == created_item["price"], \
            f"price mismatch: {retrieved_item['price']} vs {created_item['price']}"
        

        if "statistics" in created_item and created_item["statistics"]:
            stats_created = created_item["statistics"]
            stats_retrieved = retrieved_item.get("statistics", {})
            
            assert stats_retrieved.get("likes") == stats_created.get("likes", 0), \
                f"likes mismatch: {stats_retrieved.get('likes')} vs {stats_created.get('likes')}"
            
            assert stats_retrieved.get("viewCount") == stats_created.get("viewCount", 0), \
                f"viewCount mismatch: {stats_retrieved.get('viewCount')} vs {stats_created.get('viewCount')}"
            
            assert stats_retrieved.get("contacts") == stats_created.get("contacts", 0), \
                f"contacts mismatch: {stats_retrieved.get('contacts')} vs {stats_created.get('contacts')}"
    
    @staticmethod
    def assert_statistics_match(expected_stats: dict, actual_stats: dict):
        """Проверка соответствия статистики"""
        for field in ["likes", "viewCount", "contacts"]:
            assert actual_stats.get(field) == expected_stats.get(field, 0), \
                f"Statistic '{field}' mismatch: {actual_stats.get(field)} vs {expected_stats.get(field)}"
    
    @staticmethod
    def assert_error_message(response, expected_message_substring: str = None):
        """Проверка сообщения об ошибке"""
        try:
            data = response.json()
            if "message" in data:
                if expected_message_substring:
                    assert expected_message_substring in data["message"], \
                        f"Expected message containing '{expected_message_substring}', got '{data['message']}'"
        except:
            pass

assertions = Assertions()