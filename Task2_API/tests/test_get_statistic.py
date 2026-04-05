"""
Тесты получения статистики - GET /api/1/statistic/{id}
TC_012 - TC_013
"""
import pytest
from utils.assertions import assertions


@pytest.mark.smoke
@pytest.mark.positive
def test_get_statistic_by_id(api_client, created_item):
    """TC_012: Получение статистики по существующему объявлению"""
    item_id, original_data = created_item
    original_stats = original_data.get("statistics", {})

    response = api_client.get_statistic(item_id)
    assertions.assert_status_code(response, 200)

    body = response.json()
    if isinstance(body, list):
        body = body[0]

    assert "likes" in body, "Нет поля 'likes'"
    assert "viewCount" in body, "Нет поля 'viewCount'"
    assert "contacts" in body, "Нет поля 'contacts'"

    assertions.assert_statistics_match(original_stats, body)


@pytest.mark.negative
@pytest.mark.parametrize("invalid_id", [
    "1234567",
    "0",
    "null",
    "@#$%",
])
def test_get_statistic_invalid_id(api_client, invalid_id):
    """TC_013: Статистика с некорректным ID → 400 или 404"""
    response = api_client.get_statistic(invalid_id)
    assert response.status_code in [400, 404], (
        f"ID='{invalid_id}': ожидался 400/404, получен {response.status_code}"
    )
