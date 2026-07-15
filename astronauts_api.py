from __future__ import annotations

from typing import Any

from api_client import ApiClient


class AstronautsApi:
    @staticmethod
    def get_astronauts() -> dict[str, Any]:
        url = "http://api.open-notify.org/astros.json"
        return ApiClient.fetch_json(url)


def get_astronauts() -> dict[str, Any]:
    return AstronautsApi.get_astronauts()
