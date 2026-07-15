from __future__ import annotations

from typing import Any

from api_client import ApiClient

# The original boredapi.com host is no longer reachable; this community mirror
# serves the same response shape.
BORED_API_URL = "https://bored-api.appbrewery.com/random"


class BoredApi:
    @staticmethod
    def get_activity() -> dict[str, Any]:
        return ApiClient.fetch_json(BORED_API_URL)


def get_activity() -> dict[str, Any]:
    return BoredApi.get_activity()
