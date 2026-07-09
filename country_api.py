from __future__ import annotations

from typing import Any

from api_client import ApiClient


class CountryApi:
    @staticmethod
    def get_country(name: str) -> list[dict[str, Any]]:
        url = f"https://restcountries.com/v3.1/name/{name.strip()}"
        return ApiClient.fetch_json(url)

    @staticmethod
    def get_country_name_options(limit: int = 20) -> list[dict[str, str]]:
        data = ApiClient.fetch_json("https://restcountries.com/v3.1/all?fields=name")
        options = []

        for item in data[:limit]:
            country_name = item.get("name", {}).get("common")
            if country_name:
                options.append({"value": country_name, "label": country_name})

        return sorted(options, key=lambda item: item["label"])


def get_country(name: str) -> list[dict[str, Any]]:
    return CountryApi.get_country(name)


def get_country_name_options(limit: int = 20) -> list[dict[str, str]]:
    return CountryApi.get_country_name_options(limit)