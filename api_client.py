from __future__ import annotations

from typing import Any

import requests


class ApiClient:
    @staticmethod
    def fetch_json(url: str, *, headers: dict[str, str] | None = None, timeout: int = 10) -> Any:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()


def fetch_json(url: str, *, headers: dict[str, str] | None = None, timeout: int = 10) -> Any:
    return ApiClient.fetch_json(url, headers=headers, timeout=timeout)