"""
Тесты получения объявлений продавца - GET /api/1/{sellerId}/item
TC_014 - TC_015
"""
import pytest
from utils.assertions import assertions
from utils.data_generator import data_generator


@pytest.mark.smoke
@pytest.mark.positive
def test_get_all_seller_items(api_client, multiple_items_for_seller):
    """TC_014: Получение всех объявлений продавца - должен вернуться список из 3 штук"""
    seller_id, created_ids = multiple_items_for_seller

    response = api_client.get_seller_items(seller_id)
    assertions.assert_status_code(response, 200)

    items = response.json()
    assert isinstance(items, list), f"Ожидался список, получено: {type(items)}"
    assert len(items) == 3, f"Ожидалось 3 объявления, получено: {len(items)}"

    for item in items:
        assert item["sellerId"] == seller_id, (
            f"Объявление принадлежит другому продавцу: {item['sellerId']} != {seller_id}"
        )


@pytest.mark.positive
def test_get_seller_items_returns_list(api_client):
    """TC_014b: Продавец без объявлений - должен вернуться пустой список"""

    seller_id = data_generator.generate_seller_id()

    response = api_client.get_seller_items(seller_id)
    assertions.assert_status_code(response, 200)

    items = response.json()
    assert isinstance(items, list), f"Ожидался список, получено: {type(items)}"


@pytest.mark.negative
@pytest.mark.parametrize("invalid_seller_id, description", [
    (12345678123, "слишком большое"),
    ("abc",       "строка"),
    (0,           "ноль"),
])
def test_get_seller_items_invalid_id(api_client, invalid_seller_id, description):
    """TC_015: Некорректный sellerId → 400"""
    response = api_client.get_seller_items(invalid_seller_id)
    assert response.status_code == 400, (
        f"sellerId={invalid_seller_id!r} ({description}): "
        f"ожидался 400, получен {response.status_code}"
    )
