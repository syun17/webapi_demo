from __future__ import annotations

from typing import Any

from api_client import ApiClient


class IssLocationApi:
    @staticmethod
    def get_iss_location() -> dict[str, Any]:
        url = "http://api.open-notify.org/iss-now.json"
        return ApiClient.fetch_json(url)


def get_iss_location() -> dict[str, Any]:
    return IssLocationApi.get_iss_location()
