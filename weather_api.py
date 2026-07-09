from __future__ import annotations

from datetime import datetime
from typing import Any

from api_client import ApiClient


DEFAULT_WEATHER_AREA_CODE = "270000"


class WeatherApi:
    @staticmethod
    def get_weather(area_code: str = DEFAULT_WEATHER_AREA_CODE) -> dict[str, Any]:
        url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
        root = ApiClient.fetch_json(url)
        first_series = root[0]["timeSeries"][0]
        area = first_series["areas"][0]
        weather_items = []

        for time_value, weather in zip(first_series["timeDefines"], area["weathers"]):
            dt = datetime.fromisoformat(time_value)
            weather_items.append(
                {
                    "date": dt.strftime("%Y/%m/%d(%a)"),
                    "weather": weather,
                }
            )

        return {
            "area_code": area_code,
            "area_name": area.get("area", {}).get("name", "不明"),
            "items": weather_items,
        }

    @staticmethod
    def get_weather_area_options() -> list[dict[str, str]]:
        data = ApiClient.fetch_json("https://www.jma.go.jp/bosai/common/const/area.json")
        offices = data.get("offices", {})
        options = []

        for code, office in offices.items():
            name = office.get("name") or code
            options.append({"value": code, "label": f"{name} ({code})"})

        return sorted(options, key=lambda item: item["label"])


def get_weather(area_code: str = DEFAULT_WEATHER_AREA_CODE) -> dict[str, Any]:
    return WeatherApi.get_weather(area_code)


def get_weather_area_options() -> list[dict[str, str]]:
    return WeatherApi.get_weather_area_options()