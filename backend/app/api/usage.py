from fastapi import APIRouter, HTTPException
from ..schemas import UsageChartResponse, ChartDataItem, UsageItem
from ..models import Message, Report
from datetime import datetime
import re
from typing import List, Optional
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import aiohttp
import asyncio

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
    cleaned = "".join(char.lower() for char in text if char.isalnum())
    return cleaned == cleaned[::-1]


def calculate_message_credits(text: str) -> float:
    # Base cost
    credits = 1.0

    # Character count
    credits += len(text) * 0.05

    # Word length multipliers and unique word check
    words = re.findall(r"[a-zA-Z0-9]+(?:[''-][a-zA-Z0-9]+)*[''-]?", text)
    # print(words)
    unique_words = set(words)

    for word in words:
        if len(word) <= 3:
            credits += 0.1
        elif len(word) <= 7:
            credits += 0.2
        else:
            credits += 0.3

    # Third vowels
    vowels = "aeiouAEIOU"
    credits += sum(
        0.3 for i, char in enumerate(text) if (i + 1) % 3 == 0 and char in vowels
    )

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


async def get_report_details_async(report_id: int) -> Optional[Report]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{REPORTS_ENDPOINT}/{report_id}") as response:
                if response.status == 404:
                    logger.warning(
                        f"Report not found for ID {report_id}, falling back to message text calculation"
                    )
                    return None
                report_data = await response.json()
                return Report(
                    id=report_data["id"],
                    name=report_data["name"],
                    credit_cost=report_data["credit_cost"],
                )
        except aiohttp.ClientError as e:
            logger.error(f"Failed to fetch report details: {str(e)}")
            return None


async def get_current_period_messages_async() -> List[Message]:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(MESSAGES_ENDPOINT) as response:
                response.raise_for_status()
                data = await response.json()
                logger.info(f"API response data type: {type(data)}")
                logger.info(f"API response data: {data}")

                if not isinstance(data, dict) or "messages" not in data:
                    logger.error(f"Unexpected data format: {data}")
                    raise APIError("Unexpected data format received from API")

                messages_data = data["messages"]

                if not isinstance(messages_data, list):
                    logger.error(f"Messages data is not a list: {messages_data}")
                    raise APIError("Messages data is not in the expected format")

                return [
                    Message(
                        id=msg["id"],
                        text=msg["text"],
                        timestamp=datetime.fromisoformat(msg["timestamp"]),
                        report_id=msg.get("report_id"),
                    )
                    for msg in messages_data
                ]
        except aiohttp.ClientError as e:
            logger.error(f"Failed to fetch current period messages: {str(e)}")
            raise APIError(f"Failed to fetch current period messages: {str(e)}")
        except KeyError as e:
            logger.error(f"Missing key in message data: {str(e)}")
            raise APIError(f"Invalid data format: missing key {str(e)}")


async def process_message_async(message):
    credits = 0.0
    report_name = None

    if message.report_id:
        report = await get_report_details_async(message.report_id)
        if report:
            credits = report.credit_cost
            report_name = report.name
        else:
            credits = calculate_message_credits(message.text)
    else:
        credits = calculate_message_credits(message.text)

    return UsageItem(
        id=message.id,
        timestamp=message.timestamp,
        credits=round(credits, 2),
        report_name=report_name,
    )


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
        messages = await get_current_period_messages_async()

        # Process messages concurrently using asyncio.gather
        usage_items = await asyncio.gather(
            *[process_message_async(message) for message in messages]
        )

        total_credits = sum(item.credits for item in usage_items)
        chart_data = generate_chart_data(usage_items)

        return UsageChartResponse(
            usage=usage_items,
            total_credits=round(total_credits, 2),
            chart_data=chart_data,
        )
    except APIError as e:
        logger.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
