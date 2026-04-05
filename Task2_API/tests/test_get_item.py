"""
Тесты получения объявления по ID - GET /api/1/item/{id}
TC_010 - TC_011
"""
import pytest
from utils.assertions import assertions


@pytest.mark.smoke
@pytest.mark.positive
def test_get_item_by_id(api_client, created_item):
    """TC_010: Получение объявления по существующему ID"""
    item_id, original_data = created_item

    response = api_client.get_item(item_id)
    assertions.assert_status_code(response, 200)

    body = response.json()
    if isinstance(body, list):
        body = body[0]

    assert "id" in body, "Нет поля 'id' в ответе"
    assert "createdAt" in body, "Нет поля 'createdAt' в ответе"
    assert body["id"] == item_id, f"ID не совпадает: {body['id']} != {item_id}"

    assertions.assert_item_matches_original(original_data, body)


@pytest.mark.negative
@pytest.mark.parametrize("invalid_id", [
    "1234567",        
    "0",            
    "null",          
    "@#$%",           
    "999999999999",   
])
def test_get_item_invalid_id(api_client, invalid_id):
    """TC_011: Получение объявления с некорректным ID → 400 или 404"""
    response = api_client.get_item(invalid_id)
    assert response.status_code in [400, 404], (
        f"ID='{invalid_id}': ожидался 400/404, получен {response.status_code}"
    )
