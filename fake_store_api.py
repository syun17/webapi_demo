from __future__ import annotations

from typing import Any

from api_client import ApiClient


class FakeStoreApi:
    @staticmethod
    def get_products(limit: int | None = None) -> list[dict[str, Any]]:
        url = "https://fakestoreapi.com/products"
        if limit is not None:
            url += f"?limit={limit}"
        return ApiClient.fetch_json(url)


def get_products(limit: int | None = None) -> list[dict[str, Any]]:
    return FakeStoreApi.get_products(limit)
