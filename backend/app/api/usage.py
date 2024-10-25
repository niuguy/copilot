from fastapi import APIRouter, HTTPException
from ..schemas import UsageChartResponse, ChartDataItem, UsageItem
from ..models import Message, Report
import requests
from datetime import datetime
import re
from typing import List, Optional
import logging

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
API_BASE_URL = "https://owpublic.blob.core.windows.net/tech-task"
MESSAGES_ENDPOINT = f"{API_BASE_URL}/messages/current-period"
REPORTS_ENDPOINT = f"{API_BASE_URL}/reports"

class APIError(Exception):
    """Custom exception for API-related errors"""
    pass

def is_palindrome(text: str) -> bool:
    cleaned = ''.join(char.lower() for char in text if char.isalnum())
    return cleaned == cleaned[::-1]

def calculate_message_credits(text: str) -> float:
    # Base cost
    credits = 1.0
    
    # Character count
    credits += len(text) * 0.05
    
    # Word length multipliers and unique word check
    words = re.findall(r'\b[\w\'-]+\b', text)
    unique_words = set(words)
    
    for word in words:
        if len(word) <= 3:
            credits += 0.1
        elif len(word) <= 7:
            credits += 0.2
        else:
            credits += 0.3
    
    # Third vowels
    vowels = 'aeiouAEIOU'
    credits += sum(0.3 for i, char in enumerate(text) if (i + 1) % 3 == 0 and char in vowels)
    
    # Length penalty
    if len(text) > 100:
        credits += 5
    
    # Unique word bonus
    if len(words) == len(unique_words):
        credits = max(1, credits - 2)
    
    # Palindrome check
    if is_palindrome(text):
        credits *= 2
    
    return round(credits, 2)

def get_report_details(report_id: int) -> Optional[Report]:
    try:
        response = requests.get(f"{REPORTS_ENDPOINT}/{report_id}")
        response.raise_for_status()
        report_data = response.json()
        logger.info(f"Report data: {report_data}")
        return Report(
            id=report_data['id'],
            name=report_data['name'],
            credit_cost=report_data['credit_cost']
        )
    except requests.RequestException as e:
        if e.response and e.response.status_code == 404:
            logger.warning(f"Report not found for ID {report_id}, falling back to message text calculation")
            return None
        logger.error(f"Failed to fetch report details: {str(e)}")
        raise APIError(f"Failed to fetch report details: {str(e)}")

def get_current_period_messages() -> List[Message]:
    try:
        response = requests.get(MESSAGES_ENDPOINT)
        response.raise_for_status()
        data = response.json()
        logger.info(f"API response data type: {type(data)}")
        logger.info(f"API response data: {data}")

        if not isinstance(data, dict) or 'messages' not in data:
            logger.error(f"Unexpected data format: {data}")
            raise APIError("Unexpected data format received from API")

        messages_data = data['messages']

        if not isinstance(messages_data, list):
            logger.error(f"Messages data is not a list: {messages_data}")
            raise APIError("Messages data is not in the expected format")

        return [
            Message(
                id=msg['id'],
                text=msg['text'],
                timestamp=datetime.fromisoformat(msg['timestamp']),
                report_id=msg.get('report_id')
            )
            for msg in messages_data
        ]
    except requests.RequestException as e:
        logger.error(f"Failed to fetch current period messages: {str(e)}")
        raise APIError(f"Failed to fetch current period messages: {str(e)}")
    except KeyError as e:
        logger.error(f"Missing key in message data: {str(e)}")
        raise APIError(f"Invalid data format: missing key {str(e)}")

def generate_chart_data(usage_items: List[UsageItem]) -> List[ChartDataItem]:
    date_groups = {}
    for item in usage_items:
        date = item.timestamp.strftime("%d/%m/%Y")
        date_groups[date] = date_groups.get(date, 0) + item.credits

    chart_data = [
        ChartDataItem(date=date, credits=round(credits, 2))
        for date, credits in date_groups.items()
    ]
    chart_data.sort(key=lambda x: datetime.strptime(x.date, "%d/%m/%Y"))
    
    return chart_data

@router.get("/usage", response_model=UsageChartResponse)
async def get_usage():
    try:
        messages = get_current_period_messages()
        usage_items = []
        total_credits = 0.0

        for message in messages:
            credits = 0.0
            report_name = None

            if message.report_id:
                report = get_report_details(message.report_id)
                if report:
                    credits = report.credit_cost
                    report_name = report.name
                else:
                    credits = calculate_message_credits(message.text)
            else:
                credits = calculate_message_credits(message.text)

            usage_item = UsageItem(
                id=message.id,
                timestamp=message.timestamp,
                credits=round(credits, 2),
                report_name=report_name
            )

            usage_items.append(usage_item)
            total_credits += credits

        chart_data = generate_chart_data(usage_items)

        return UsageChartResponse(
            usage=usage_items,
            total_credits=round(total_credits, 2),
            chart_data=chart_data
        )
    except APIError as e:
        logger.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
