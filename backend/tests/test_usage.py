import sys
from pathlib import Path
import pytest
from datetime import datetime
import requests_mock

# Add the parent directory of 'app' to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from app.api.usage import (
    calculate_message_credits,
    get_report_details,
    get_usage,
    is_palindrome
)
from app.schemas import UsageChartResponse
from app.models import Report

def test_is_palindrome():
    assert is_palindrome("A man a plan a canal Panama") == True
    assert is_palindrome("race a car") == False
    assert is_palindrome("Was it a car or a cat I saw?") == True
    assert is_palindrome("hello world") == False
    assert is_palindrome("") == True
    assert is_palindrome("aaa") == True

def test_calculate_message_credits():
    #one word(no palindrome)  = base cost + 0.05 for each character + length multiplier 1-3 charac
    assert calculate_message_credits("ab") == 1.2 #1 + 0.05*2 + 0.1*1
    #one word(no palindrome)  = base cost + 0.05 for each character + length multiplier 4-6 characters
    assert calculate_message_credits("word") == 1.4 #1 + 0.05*4+ 0.2*1
    #one word(no palindrome)  = base cost + 0.05 for each character + length multiplier 7-9 characters
    assert calculate_message_credits("wordssss") == 1.6 #1 + 0.05*8+ 0.3*1
    #three words(no palindrome,no unique words) = base cost + 0.05 for each character + length multiplier
    # assert calculate_message_credits("key key key") == 1.9 #1 + 0.05*9 + 0.1*3

    # #palindrome = 2 * base cost + 0.05 for each character
    # assert calculate_message_credits("A man a plan a canal Panama") == 7.46 #2*1 + 0.05*28

    # #unique words only = base cost + 0.05 for each character - 2
    # assert calculate_message_credits("The quick brown fox jumps over the lazy dog") == 5.75 #1 + 0.05*19 - 2
    # assert calculate_message_credits("A" * 101) == 13.95