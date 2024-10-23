from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime
import re
from typing import List, Dict, Optional
from pydantic import BaseModel

# Data models
class Message(BaseModel):
    id: int
    text: str
    timestamp: datetime
    report_id: Optional[int] = None

class Report(BaseModel):
    id: int
    name: str
    credit_cost: float

class UsageItem(BaseModel):
    id: int
    timestamp: datetime
    report_name: Optional[str] = None
    credits: float

class UsageResponse(BaseModel):
    usage: List[UsageItem]
    total_credits: float

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
API_BASE_URL = "https://owpublic.blob.core.windows.net/tech-task"
MESSAGES_ENDPOINT = f"{API_BASE_URL}/messages/current-period"
REPORTS_ENDPOINT = f"{API_BASE_URL}/reports"

class APIError(Exception):
    """Custom exception for API-related errors"""
    pass

def calculate_message_credits(text: str) -> float:
    # Initialize with base cost
    credits = 1.0
    
    # Character count (0.05 credits per character)
    credits += len(text) * 0.05
    
    # Word analysis
    words = re.findall(r"[a-zA-Z'-]+", text)
    
    # Word length multipliers
    for word in words:
        if len(word) <= 3:
            credits += 0.1
        elif len(word) <= 7:
            credits += 0.2
        else:
            credits += 0.3
    
    # Third vowels check
    vowels = set('aeiouAEIOU')
    for i in range(2, len(text), 3):
        if text[i] in vowels:
            credits += 0.3
    
    # Length penalty
    if len(text) > 100:
        credits += 5
    
    # Unique word bonus
    if len(words) == len(set(words)):
        credits = max(1, credits - 2)
    
    # Palindrome check
    cleaned_text = ''.join(c.lower() for c in text if c.isalnum())
    if cleaned_text == cleaned_text[::-1]:
        credits *= 2
    
    return max(1, round(credits, 2))

def get_report_details(report_id: int) -> Optional[Report]:
    try:
        response = requests.get(f"{REPORTS_ENDPOINT}/{report_id}")
        if response.status_code == 200:
            data = response.json()
            return Report(**data)
        elif response.status_code == 404:
            return None
        else:
            raise APIError(f"Report API returned status code {response.status_code}")
    except requests.RequestException as e:
        raise APIError(f"Failed to fetch report details: {str(e)}")

def get_current_period_messages() -> List[Message]:
    try:
        response = requests.get(MESSAGES_ENDPOINT)
        if response.status_code == 200:
            messages_data = response.json().get("messages", [])
            return [Message(**msg) for msg in messages_data]
        else:
            raise APIError(f"Messages API returned status code {response.status_code}")
    except requests.RequestException as e:
        raise APIError(f"Failed to fetch messages: {str(e)}")

@app.get("/usage", response_model=UsageResponse)
async def get_usage():
    try:
        messages = get_current_period_messages()
        usage_items = []
        total_credits = 0.0

        for message in messages:
            credits = 0.0
            report_name = None

            if message.report_id:
                try:
                    report = get_report_details(message.report_id)
                    if report:
                        credits = report.credit_cost
                        report_name = report.name
                    else:
                        credits = calculate_message_credits(message.text)
                except APIError:
                    credits = calculate_message_credits(message.text)
            else:
                credits = calculate_message_credits(message.text)

            usage_item = UsageItem(
                id=message.id,
                timestamp=message.timestamp,
                credits=round(credits, 2)
            )
            
            if report_name:
                usage_item.report_name = report_name

            usage_items.append(usage_item)
            total_credits += credits

        return UsageResponse(
            usage=usage_items,
            total_credits=round(total_credits, 2)
        )
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)