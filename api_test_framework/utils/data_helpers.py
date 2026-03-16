"""
Test Data Helpers
Loads JSON fixtures and generates dynamic payloads.
"""

import json
import random
import string
import uuid
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "tests" / "test_data"


def load_fixture(filename: str) -> dict | list:
    """Load a JSON fixture from tests/test_data/."""
    path = DATA_DIR / filename
    with open(path) as f:
        return json.load(f)


def random_string(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email() -> str:
    return f"{random_string(6)}@{random_string(4)}.com"


def random_uuid() -> str:
    return str(uuid.uuid4())


def random_int(low: int = 1, high: int = 1000) -> int:
    return random.randint(low, high)


def make_user_payload(name: str = None, email: str = None, age: int = None) -> dict:
    return {
        "name": name or random_string(8).capitalize(),
        "email": email or random_email(),
        "age": age or random_int(18, 65),
    }


def make_post_payload(title: str = None, body: str = None, user_id: int = None) -> dict:
    return {
        "title": title or f"Post {random_string(5)}",
        "body": body or f"Body text {random_string(20)}.",
        "userId": user_id or random_int(1, 10),
    }
