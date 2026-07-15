from __future__ import annotations

from typing import Any

from api_client import ApiClient


class ZippopotamusApi:
    @staticmethod
    def get_postal_info(country: str, postal_code: str) -> dict[str, Any]:
        url = f"https://api.zippopotam.us/{country.strip()}/{postal_code.strip()}"
        return ApiClient.fetch_json(url)


def get_postal_info(country: str, postal_code: str) -> dict[str, Any]:
    return ZippopotamusApi.get_postal_info(country, postal_code)
