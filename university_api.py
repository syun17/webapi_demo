from __future__ import annotations

from typing import Any

from api_client import ApiClient


class UniversityApi:
    @staticmethod
    def search_universities(country: str) -> list[dict[str, Any]]:
        url = f"http://universities.hipolabs.com/search?country={country.strip()}"
        return ApiClient.fetch_json(url)


def search_universities(country: str) -> list[dict[str, Any]]:
    return UniversityApi.search_universities(country)
