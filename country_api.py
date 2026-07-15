from __future__ import annotations

from typing import Any

from api_client import ApiClient

# restcountries.com's v3.1 endpoint was deprecated and now requires a paid
# authorization key. This reads the same dataset restcountries.com is built
# from, straight from its open-source GitHub repo via the jsDelivr CDN, and
# filters it locally instead.
COUNTRIES_DATA_URL = (
    "https://cdn.jsdelivr.net/gh/restcountries/restcountries@master/"
    "src/main/resources/countriesV3.1.json"
)

_countries_cache: list[dict[str, Any]] | None = None


class CountryApi:
    @staticmethod
    def _load_countries() -> list[dict[str, Any]]:
        global _countries_cache
        if _countries_cache is None:
            _countries_cache = ApiClient.fetch_json(COUNTRIES_DATA_URL)
        return _countries_cache

    @staticmethod
    def get_country(name: str) -> list[dict[str, Any]]:
        query = name.strip().lower()
        matches = [
            country
            for country in CountryApi._load_countries()
            if query in country.get("name", {}).get("common", "").lower()
        ]
        if not matches:
            raise ValueError(f"'{name}' に一致する国が見つかりませんでした。")
        return matches

    @staticmethod
    def get_country_name_options(limit: int = 20) -> list[dict[str, str]]:
        data = CountryApi._load_countries()
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
