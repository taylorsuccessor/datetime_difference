from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_validation_empty_json():

    response = client.post("/api/difference-between-dates", json={})
    assert response.status_code == 422

    response = client.post("/api/difference-between-dates", json="")
    assert response.status_code == 422


def test_validate_datetime():

    json = {
        "from_datetime": "2022-13-01T00:00:00+00:00",
        "to_datetime": "2022-13-05T00:00:00+00:00",
    }
    response = client.post("/api/difference-between-dates", json=json)
    assert response.status_code == 422

    expected_reqsponse = {
        "detail": [
            {
                "loc": ["body", "from_datetime"],
                "msg": "invalid datetime format",
                "type": "value_error.datetime",
            },
            {
                "loc": ["body", "to_datetime"],
                "msg": "invalid datetime format",
                "type": "value_error.datetime",
            },
        ]
    }

    assert response.json() == expected_reqsponse


def test_validate_response_type_unit():

    json = {
        "from_datetime": "2022-04-01T00:00:00+00:00",
        "to_datetime": "2022-04-05T00:00:00+00:00",
        "response_type": "not_an_option",
    }

    response = client.post("/api/difference-between-dates", json=json)
    assert response.status_code == 422

    expected_reqsponse = {
        "detail": [
            {
                "loc": ["body", "response_type"],
                "msg": "value is not a valid enumeration member; permitted: 'seconds', 'minutes', 'hours', 'days', 'weeks', 'years'",
                "type": "type_error.enum",
                "ctx": {
                    "enum_values": [
                        "seconds",
                        "minutes",
                        "hours",
                        "days",
                        "weeks",
                        "years",
                    ]
                },
            }
        ]
    }

    assert response.json() == expected_reqsponse


def test_get_days_difference():

    json = {
        "from_datetime": "2022-04-01T00:00:00+00:00",
        "to_datetime": "2022-04-05T00:00:00+00:00",
    }
    response = client.post("/api/difference-between-dates", json=json)
    assert response.status_code == 200

    expected_reqsponse = {"days_number": 4, "weekdays_number": 2, "weeks_number": 0.571}

    assert response.json() == expected_reqsponse


def test_get_weeks_difference():

    json = {
        "from_datetime": "2022-04-01T00:00:00+00:00",
        "to_datetime": "2022-05-05T00:00:00+00:00",
    }
    response = client.post("/api/difference-between-dates", json=json)
    assert response.status_code == 200

    expected_reqsponse = {
        "days_number": 34,
        "weekdays_number": 24,
        "weeks_number": 4.857,
    }

    assert response.json() == expected_reqsponse


def test_get_calculate_timezone_difference():

    json = {
        "from_datetime": "2022-04-01T00:00:00+23:00",
        "to_datetime": "2022-04-01T00:00:00+00:00",
    }
    response = client.post("/api/difference-between-dates", json=json)
    assert response.status_code == 200

    expected_reqsponse = {
        "days_number": 0.958,
        "weekdays_number": 0,
        "weeks_number": 0.137,
    }

    assert response.json() == expected_reqsponse


def test_convert_response_unit():

    json = {
        "from_datetime": "2022-04-01T00:00:00+00:00",
        "to_datetime": "2022-04-08T00:00:00+00:00",
    }
    response = client.post("/api/difference-between-dates", json=json)
    assert response.status_code == 200

    expected_reqsponse = {"days_number": 7, "weekdays_number": 5, "weeks_number": 1}

    assert response.json() == expected_reqsponse

    json["response_type"] = "seconds"

    response = client.post("/api/difference-between-dates", json=json)

    expected_reqsponse = {
        "days_number": 604800,
        "weekdays_number": 432000,
        "weeks_number": 604800,
    }

    assert response.json() == expected_reqsponse

    json["response_type"] = "minutes"

    response = client.post("/api/difference-between-dates", json=json)

    expected_reqsponse = {
        "days_number": 10080,
        "weekdays_number": 7200,
        "weeks_number": 10080,
    }

    assert response.json() == expected_reqsponse

    json["response_type"] = "hours"

    response = client.post("/api/difference-between-dates", json=json)

    expected_reqsponse = {
        "days_number": 168,
        "weekdays_number": 120,
        "weeks_number": 168,
    }

    assert response.json() == expected_reqsponse

    json["response_type"] = "days"

    response = client.post("/api/difference-between-dates", json=json)

    expected_reqsponse = {"days_number": 7, "weekdays_number": 5, "weeks_number": 7}

    assert response.json() == expected_reqsponse

    json["response_type"] = "weeks"

    response = client.post("/api/difference-between-dates", json=json)

    expected_reqsponse = {"days_number": 1, "weekdays_number": 0.714, "weeks_number": 1}

    assert response.json() == expected_reqsponse

    json["response_type"] = "years"

    response = client.post("/api/difference-between-dates", json=json)

    expected_reqsponse = {
        "days_number": 0.019,
        "weekdays_number": 0.014,
        "weeks_number": 0.019,
    }

    assert response.json() == expected_reqsponse


def test_get_fractions_difference():

    json = {
        "from_datetime": "2022-04-01T00:00:00+05:00",
        "to_datetime": "2022-04-01T00:00:00+00:00",
    }
    response = client.post("/api/difference-between-dates", json=json)
    assert response.status_code == 200

    expected_reqsponse = {
        "days_number": 0.208,
        "weekdays_number": 0,
        "weeks_number": 0.03,
    }

    assert response.json() == expected_reqsponse
