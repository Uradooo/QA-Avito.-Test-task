import pytest
from utils.api_client import APIClient
from utils.data_generator import data_generator


@pytest.fixture(scope="session")
def api_client():
    """API клиент - создаётся один раз на всю сессию тестов"""
    return APIClient()


@pytest.fixture
def test_item_data():
    """Генерирует данные для нового объявления"""
    return data_generator.generate_valid_item()


@pytest.fixture
def created_item(api_client, test_item_data):
    """
    Создаёт объявление перед тестом и удаляет его после.
    Возвращает (item_id, данные_объявления).
    """
    response = api_client.create_item(test_item_data)
    assert response.status_code == 200, f"Не удалось создать объявление: {response.text}"

    item_id = api_client.extract_item_id(response)
    assert item_id is not None, f"Не удалось извлечь ID из ответа: {response.text}"

    yield item_id, test_item_data

    try:
        api_client.delete_item(item_id)
    except Exception:
        pass


@pytest.fixture
def multiple_items_for_seller(api_client):
    """
    Создаёт 3 объявления для одного продавца.
    Возвращает (seller_id, [id1, id2, id3]).
    """
    seller_id = data_generator.generate_seller_id()
    created_ids = []

    for _ in range(3):
        item_data = data_generator.generate_valid_item(seller_id)
        response = api_client.create_item(item_data)
        assert response.status_code == 200, f"Не удалось создать объявление: {response.text}"
        item_id = api_client.extract_item_id(response)
        assert item_id is not None
        created_ids.append(item_id)

    yield seller_id, created_ids

    for item_id in created_ids:
        try:
            api_client.delete_item(item_id)
        except Exception:
            pass
