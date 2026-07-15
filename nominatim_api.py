from __future__ import annotations

from typing import Any

from api_client import ApiClient

# Nominatim's usage policy requires a distinct User-Agent for every client.
NOMINATIM_HEADERS = {"User-Agent": "webapi-demo/1.0"}


class NominatimApi:
    @staticmethod
    def search_location(query: str) -> list[dict[str, Any]]:
        url = f"https://nominatim.openstreetmap.org/search?q={query.strip()}&format=json&addressdetails=1"
        return ApiClient.fetch_json(url, headers=NOMINATIM_HEADERS)


def search_location(query: str) -> list[dict[str, Any]]:
    return NominatimApi.search_location(query)
