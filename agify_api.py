from __future__ import annotations

from typing import Any

from api_client import ApiClient


class AgifyApi:
    @staticmethod
    def get_age_prediction(name: str) -> dict[str, Any]:
        url = f"https://api.agify.io/?name={name.strip()}"
        return ApiClient.fetch_json(url)


def get_age_prediction(name: str) -> dict[str, Any]:
    return AgifyApi.get_age_prediction(name)
