from __future__ import annotations

from typing import Any

from api_client import ApiClient


class CountriesNowApi:
    @staticmethod
    def get_all_countries() -> dict[str, Any]:
        url = "https://countriesnow.space/api/v0.1/countries"
        return ApiClient.fetch_json(url)


def get_all_countries() -> dict[str, Any]:
    return CountriesNowApi.get_all_countries()
