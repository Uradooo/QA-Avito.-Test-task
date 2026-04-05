"""
Тесты создания объявлений - POST /api/1/item
TC_001 - TC_009
"""
import pytest
from utils.data_generator import data_generator
from utils.assertions import assertions


#Позитивные тесты 

@pytest.mark.smoke
@pytest.mark.positive
def test_create_item_typical(api_client):
    """TC_001: Создание объявления с типовыми данными"""
    item_data = {
        "sellerId": 111112,
        "name": "Первый тест",
        "price": 1000,
        "statistics": {"contacts": 10, "likes": 10, "viewCount": 100},
    }

    response = api_client.create_item(item_data)
    assertions.assert_status_code(response, 200)

    body = response.json()
    assert "status" in body
    assert "Сохранили объявление" in body["status"]

    item_id = api_client.extract_item_id(response)
    assert item_id is not None

    get_resp = api_client.get_item(item_id)
    assertions.assert_status_code(get_resp, 200)

    saved = get_resp.json()
    if isinstance(saved, list):
        saved = saved[0]

    assertions.assert_item_matches_original(item_data, saved)
    api_client.delete_item(item_id)


@pytest.mark.positive
@pytest.mark.boundary
def test_create_item_max_seller_id(api_client):
    """TC_002: sellerId на верхней границе (999999)"""
    item_data = data_generator.generate_valid_item(seller_id=999999)

    response = api_client.create_item(item_data)
    assertions.assert_status_code(response, 200)

    item_id = api_client.extract_item_id(response)
    get_resp = api_client.get_item(item_id)
    saved = get_resp.json()
    if isinstance(saved, list):
        saved = saved[0]

    assert saved["sellerId"] == 999999
    api_client.delete_item(item_id)


@pytest.mark.positive
@pytest.mark.boundary
def test_create_item_min_seller_id(api_client):
    """TC_003: sellerId на нижней границе (111111)"""
    item_data = data_generator.generate_valid_item(seller_id=111111)

    response = api_client.create_item(item_data)
    assertions.assert_status_code(response, 200)

    item_id = api_client.extract_item_id(response)
    get_resp = api_client.get_item(item_id)
    saved = get_resp.json()
    if isinstance(saved, list):
        saved = saved[0]

    assert saved["sellerId"] == 111111
    api_client.delete_item(item_id)


#Негативные тесты: sellerId

@pytest.mark.negative
@pytest.mark.parametrize("invalid_seller_id, description", [
    (None,      "null"),
    ("abc123",  "строка"),
    (1000000,   "выше диапазона"),
    (111110,    "ниже диапазона"),
    (-1,        "отрицательное"),
])
def test_create_item_invalid_seller_id(api_client, invalid_seller_id, description):
    """TC_004: sellerId с некорректными значениями → 400
    
    ВНИМАНИЕ: API принимает некорректные значения (баги BUG_001, BUG_002).
    Тест упадёт - это ожидаемо, см. BUGS.md.
    """
    item_data = data_generator.generate_valid_item()
    item_data["sellerId"] = invalid_seller_id

    response = api_client.create_item(item_data)
    assert response.status_code == 400, (
        f"sellerId={invalid_seller_id!r} ({description}): "
        f"ожидался 400, получен {response.status_code}"
    )


#Негативные тесты: обязательные поля

@pytest.mark.negative
@pytest.mark.parametrize("missing_field", ["sellerId", "name", "price", "statistics"])
def test_create_item_missing_required_field(api_client, missing_field):
    """TC_005: Отсутствие обязательного поля → 400"""
    item_data = data_generator.generate_valid_item()
    del item_data[missing_field]

    response = api_client.create_item(item_data)
    assertions.assert_status_code(response, 400)

    body = response.json()
    assert "message" in body or "status" in body


#Негативные тесты: name

@pytest.mark.negative
@pytest.mark.parametrize("invalid_name, description", [
    (None,        "null"),
    ("",          "пустая строка"),
    ("a",         "слишком короткое"),
    ("   ",       "только пробелы"),
    ("a" * 2000,  "слишком длинное"),
    (-1,          "число отрицательное"),
    (123,         "число"),
])
def test_create_item_invalid_name(api_client, invalid_name, description):
    """TC_006: Поле name с некорректными значениями → 400
    
    ВНИМАНИЕ: пробелы и спецсимволы принимаются (баги BUG_003, BUG_004).
    """
    item_data = data_generator.generate_valid_item()
    item_data["name"] = invalid_name

    response = api_client.create_item(item_data)
    assert response.status_code == 400, (
        f"name={invalid_name!r} ({description}): "
        f"ожидался 400, получен {response.status_code}"
    )


#Негативные тесты: price

@pytest.mark.negative
@pytest.mark.parametrize("invalid_price, description", [
    (None,      "null"),
    (0,         "ноль"),
    (10**13,    "превышает максимум"),
    (-1,        "отрицательное"),
    ("123abc",  "строка"),
])
def test_create_item_invalid_price(api_client, invalid_price, description):
    """TC_007: Поле price с некорректными значениями → 400
    
    ВНИМАНИЕ: отрицательная цена принимается (баг BUG_005).
    Цена 0 - спорный случай, тест помечает как ожидаемый сбой.
    """
    item_data = data_generator.generate_valid_item()
    item_data["price"] = invalid_price

    response = api_client.create_item(item_data)

    if description == "ноль":

        assert response.status_code in [200, 400], (
            f"price=0: ожидался 200 или 400, получен {response.status_code}"
        )
    else:
        assert response.status_code == 400, (
            f"price={invalid_price!r} ({description}): "
            f"ожидался 400, получен {response.status_code}"
        )


#Негативные тесты: statistics

@pytest.mark.negative
@pytest.mark.parametrize("invalid_stats, description", [
    (None,                                          "null"),
    ("invalid",                                     "строка"),
    (-1,                                            "число"),
    ({"likes": "abc", "viewCount": 100, "contacts": 10}, "некорректный тип поля"),
])
def test_create_item_invalid_statistics(api_client, invalid_stats, description):
    """TC_008: Поле statistics с некорректными значениями → 400
    
    ВНИМАНИЕ: отрицательные значения принимаются (баг BUG_006).
    """
    item_data = data_generator.generate_valid_item()
    item_data["statistics"] = invalid_stats

    response = api_client.create_item(item_data)
    assert response.status_code == 400, (
        f"statistics={invalid_stats!r} ({description}): "
        f"ожидался 400, получен {response.status_code}"
    )


#Пустое тело

@pytest.mark.negative
def test_create_item_empty_body(api_client):
    """TC_009: Пустое тело запроса → 400"""
    response = api_client.create_item({})
    assertions.assert_status_code(response, 400)
