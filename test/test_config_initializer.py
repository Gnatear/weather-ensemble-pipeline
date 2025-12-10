from config.initializer import (
    DEFAULT_CITY,
    DEFAULT_DAYS,
    DEFAULT_LAT,
    DEFAULT_LON,
    API_KEYS,
)

def test_deafult_city_and_days():
    assert isinstance(DEFAULT_CITY, str)
    assert DEFAULT_CITY.lower() == "halifax"
    assert isinstance(DEFAULT_DAYS, int)
    assert DEFAULT_DAYS == 7

def test_default_coordinates_type():
    assert isinstance(DEFAULT_LAT, float)
    assert isinstance(DEFAULT_LON, float)

def test_api_keys_structure():
    assert isinstance(API_KEYS, dict)
    # does not care if is none. only check existance
    expected_keys = {
        "weatherapi",
        "visualcrossing",
        "openweather",
        "tomorrow",
        "weatherbit",
        "stormglass",
    }
    # all the keys must in API.KEYS
    assert expected_keys.issubset(API_KEYS.keys())