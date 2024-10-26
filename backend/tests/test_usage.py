import sys
from pathlib import Path
# Add the parent directory of 'app' to the Python path
sys.path.append(str(Path(__file__).parent.parent))
from datetime import datetime
import requests_mock
from fastapi.testclient import TestClient
from app.api.usage import (
    calculate_message_credits,
    get_report_details,
    get_usage,
    get_current_period_messages,
    generate_chart_data,
    router,
    is_palindrome,
)
from app.schemas import UsageChartResponse, UsageItem, ChartDataItem
from app.models import Report, Message

client = TestClient(router)


def test_get_current_period_messages(requests_mock):
    mock_response = {
        "messages": [
            {
                "id": 1,
                "text": "Hello",
                "timestamp": "2023-04-01T12:00:00",
                "report_id": None,
            },
            {
                "id": 2,
                "text": "World",
                "timestamp": "2023-04-02T12:00:00",
                "report_id": 1,
            },
        ]
    }
    requests_mock.get(
        "https://owpublic.blob.core.windows.net/tech-task/messages/current-period",
        json=mock_response,
    )

    messages = get_current_period_messages()

    assert len(messages) == 2
    assert messages[0].id == 1
    assert messages[0].text == "Hello"
    assert messages[0].timestamp == datetime(2023, 4, 1, 12, 0)
    assert messages[0].report_id is None


def test_get_report_details(requests_mock):
    mock_response = {"id": 1, "name": "Test Report", "credit_cost": 5.0}
    requests_mock.get(
        "https://owpublic.blob.core.windows.net/tech-task/reports/1", json=mock_response
    )

    report = get_report_details(1)

    assert report.id == 1
    assert report.name == "Test Report"
    assert report.credit_cost == 5.0


def test_generate_chart_data():
    usage_items = [
        UsageItem(id=1, timestamp=datetime(2023, 4, 1), credits=1.5, report_name=None),
        UsageItem(id=2, timestamp=datetime(2023, 4, 1), credits=2.5, report_name=None),
        UsageItem(id=3, timestamp=datetime(2023, 4, 2), credits=3.0, report_name=None),
    ]

    chart_data = generate_chart_data(usage_items)

    assert len(chart_data) == 2
    assert chart_data[0] == ChartDataItem(date="01/04/2023", credits=4.0)
    assert chart_data[1] == ChartDataItem(date="02/04/2023", credits=3.0)


def test_is_palindrome():
    assert is_palindrome("A man a plan a canal Panama") == True
    assert is_palindrome("race a car") == False
    assert is_palindrome("Was it a car or a cat I saw?") == True
    assert is_palindrome("hello world") == False
    assert is_palindrome("") == True
    assert is_palindrome("aaa") == True


def test_calculate_message_credits():
    # one short word,unique bonus
    assert calculate_message_credits("ab") == 1  # max(1, 1 + 0.05*2 + 0.1*1-2)
    # two short words, no unique bonus
    assert calculate_message_credits("bc bc") == 1.45  # 1 + 0.05*5 + 0.1*2

    # two short words, unique bonus
    assert calculate_message_credits("bc cd") == 1  # max(1,1 + 0.05*5 + 0.1*2-2)
    # two medium words, no unique bonus
    assert calculate_message_credits("bcdg bcdg") == 1.85  # 1 + 0.05*9 + 0.2*2
    # two long words, no unique bonus
    assert calculate_message_credits("bcdgktlq bcdgktlq") == 2.45  # 1 + 0.05*17 + 0.3*2

    # change above case to include special characters
    assert calculate_message_credits("bc'gktlq bc'gktlq") == 2.45  # 1 + 0.05*17 + 0.3*2
    assert calculate_message_credits("bc-gktlq bc-gktlq") == 2.45  # 1 + 0.05*17 + 0.3*2

    # change above case to include vowels at 3rd position
    assert calculate_message_credits("bcEgktlq bcEgktlq") == 3.05  # 2.45+0.3*2
    assert calculate_message_credits("bcegktlq bcegktlq") == 3.05  # 2.45+0.3*2

    # length penalty
    assert (
        calculate_message_credits(
            "cfpgvbxhpyxkjnsjfdzhvdcrjybdyjcmnzbqnjncmdzljgfhky cfpgvbxhpyxkjnsjfdzhvdcrjybdyjcmnzbqnjncmdzljgfhky"
        )
        == 11.65
    )  # 1+ 0.05*101 +0.3*2+5
    # palindrome penalty
    assert calculate_message_credits("kbccbk") == 2  # 2*(1 + 0.05*6+0.02 -2)


def test_get_usage(requests_mock):
    # Mock the current period messages
    mock_messages = {
        "messages": [
            {
                "id": 1,
                "text": "Hello",
                "timestamp": "2023-04-01T12:00:00",
                "report_id": None,
            },
            {
                "id": 2,
                "text": "World",
                "timestamp": "2023-04-02T12:00:00",
                "report_id": 1,
            },
        ]
    }
    requests_mock.get(
        "https://owpublic.blob.core.windows.net/tech-task/messages/current-period",
        json=mock_messages,
    )

    # Mock the report details
    mock_report = {"id": 1, "name": "Test Report", "credit_cost": 5.0}
    requests_mock.get(
        "https://owpublic.blob.core.windows.net/tech-task/reports/1", json=mock_report
    )

    response = client.get("/usage")
    assert response.status_code == 200

    data = response.json()
    assert "usage" in data
    assert "total_credits" in data
    assert "chart_data" in data
