"""
Response Validator Module
Provides chainable assertions for API response validation.
"""

import json
import logging
from typing import Any, List, Optional
import jsonschema
import requests

logger = logging.getLogger(__name__)


class ResponseValidator:
    def __init__(self, response: requests.Response):
        self.response = response
        self._json = None

    @property
    def json(self) -> Any:
        if self._json is None:
            try:
                self._json = self.response.json()
            except Exception:
                self._json = {}
        return self._json

    # ── Status ──────────────────────────────────────────────────────────────
    def status_code(self, expected: int) -> "ResponseValidator":
        actual = self.response.status_code
        assert actual == expected, f"Expected status {expected}, got {actual}.\nBody: {self.response.text[:500]}"
        logger.info(f"✔ Status code: {actual}")
        return self

    def status_ok(self) -> "ResponseValidator":
        return self.status_code(200)

    def status_created(self) -> "ResponseValidator":
        return self.status_code(201)

    def status_no_content(self) -> "ResponseValidator":
        return self.status_code(204)

    def status_in(self, codes: List[int]) -> "ResponseValidator":
        actual = self.response.status_code
        assert actual in codes, f"Expected one of {codes}, got {actual}"
        return self

    # ── Body / JSON ──────────────────────────────────────────────────────────
    def body_contains_key(self, key: str) -> "ResponseValidator":
        assert key in self.json, f"Key '{key}' not found in response: {self.json}"
        return self

    def body_value_equals(self, key: str, expected: Any) -> "ResponseValidator":
        actual = self.json.get(key)
        assert actual == expected, f"'{key}': expected '{expected}', got '{actual}'"
        return self

    def body_value_not_null(self, key: str) -> "ResponseValidator":
        value = self.json.get(key)
        assert value is not None, f"'{key}' is null or missing"
        return self

    def body_is_list(self) -> "ResponseValidator":
        assert isinstance(self.json, list), f"Expected list, got {type(self.json)}"
        return self

    def body_list_not_empty(self) -> "ResponseValidator":
        self.body_is_list()
        assert len(self.json) > 0, "Response list is empty"
        return self

    def body_matches_schema(self, schema: dict) -> "ResponseValidator":
        try:
            jsonschema.validate(instance=self.json, schema=schema)
            logger.info("✔ Schema validation passed")
        except jsonschema.ValidationError as e:
            raise AssertionError(f"Schema validation failed: {e.message}")
        return self

    # ── Headers ──────────────────────────────────────────────────────────────
    def header_equals(self, header: str, value: str) -> "ResponseValidator":
        actual = self.response.headers.get(header, "")
        assert actual == value, f"Header '{header}': expected '{value}', got '{actual}'"
        return self

    def header_contains(self, header: str, substring: str) -> "ResponseValidator":
        actual = self.response.headers.get(header, "")
        assert substring in actual, f"Header '{header}' ('{actual}') does not contain '{substring}'"
        return self

    def content_type_json(self) -> "ResponseValidator":
        return self.header_contains("Content-Type", "application/json")

    # ── Performance ──────────────────────────────────────────────────────────
    def response_time_under(self, ms: int) -> "ResponseValidator":
        elapsed = self.response.elapsed.total_seconds() * 1000
        assert elapsed < ms, f"Response took {elapsed:.0f}ms, expected < {ms}ms"
        logger.info(f"✔ Response time: {elapsed:.0f}ms")
        return self

    # ── Helpers ──────────────────────────────────────────────────────────────
    def dump(self) -> "ResponseValidator":
        logger.debug(f"Status: {self.response.status_code}")
        logger.debug(f"Headers: {dict(self.response.headers)}")
        logger.debug(f"Body: {json.dumps(self.json, indent=2)}")
        return self


def validate(response: requests.Response) -> ResponseValidator:
    """Convenience factory: validate(response).status_ok().body_contains_key('id')"""
    return ResponseValidator(response)
