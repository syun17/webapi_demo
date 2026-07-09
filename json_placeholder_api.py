from __future__ import annotations

from typing import Any

from api_client import ApiClient


class JsonPlaceholderApi:
    @staticmethod
    def get_post(post_id: int) -> dict[str, Any]:
        url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
        return ApiClient.fetch_json(url)

    @staticmethod
    def get_post_id_options(limit: int = 10) -> list[dict[str, str]]:
        data = ApiClient.fetch_json("https://jsonplaceholder.typicode.com/posts")
        unique_ids = []
        seen_ids = set()

        for item in data:
            post_id = item.get("id")
            if post_id in seen_ids:
                continue
            seen_ids.add(post_id)
            unique_ids.append({"value": str(post_id), "label": str(post_id)})
            if len(unique_ids) >= limit:
                break

        return unique_ids


def get_post(post_id: int) -> dict[str, Any]:
    return JsonPlaceholderApi.get_post(post_id)


def get_post_id_options(limit: int = 10) -> list[dict[str, str]]:
    return JsonPlaceholderApi.get_post_id_options(limit)