from __future__ import annotations

import json

from flask import Flask, render_template, request

from wether import (
	get_country,
	get_joke,
	get_picsum_url,
	get_post,
	get_pokemon,
	get_random_user,
	get_weather,
)

app = Flask(__name__)


API_CARDS = [
	{
		"title": "気象庁 天気予報API",
		"description": "予報区コードを指定して今日の天気予報を取得します。",
		"path": "/weather",
		"placeholder": "270000",
	},
	{
		"title": "PokeAPI",
		"description": "ポケモン名を指定して、タイプや図鑑情報を取得します。",
		"path": "/pokemon",
		"placeholder": "pikachu",
	},
	{
		"title": "JSONPlaceholder",
		"description": "投稿IDを指定してテスト用投稿データを取得します。",
		"path": "/post",
		"placeholder": "1",
	},
	{
		"title": "Icanhazdadjoke API",
		"description": "ランダムなダジャレを取得します。",
		"path": "/joke",
		"placeholder": "",
	},
	{
		"title": "REST Countries API",
		"description": "国名を指定して首都や人口などの情報を取得します。",
		"path": "/country",
		"placeholder": "Japan",
	},
	{
		"title": "Random User API",
		"description": "ランダムなユーザー情報を取得します。",
		"path": "/user",
		"placeholder": "",
	},
	{
		"title": "Lorem Picsum",
		"description": "ランダムな画像URLを生成して表示します。",
		"path": "/image",
		"placeholder": "",
	},
]


def render_dashboard(**context):
	return render_template(
		"index.html",
		api_cards=API_CARDS,
		**context,
	)


@app.get("/")
def index():
	return render_dashboard()


@app.get("/weather")
def weather():
	area_code = request.args.get("area_code", "270000").strip() or "270000"
	try:
		data = get_weather(area_code)
		summary = f"{data['area_name']} の天気予報を取得しました。"
		return render_dashboard(
			active_api="weather",
			panel_title="気象庁 天気予報API",
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_dashboard(
			active_api="weather",
			panel_title="気象庁 天気予報API",
			error=str(exc),
		)


@app.get("/pokemon")
def pokemon():
	name = request.args.get("name", "pikachu").strip() or "pikachu"
	try:
		data = get_pokemon(name)
		summary = f"{data['name'].title()} の情報を取得しました。"
		return render_dashboard(
			active_api="pokemon",
			panel_title="PokeAPI",
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_dashboard(
			active_api="pokemon",
			panel_title="PokeAPI",
			error=str(exc),
		)


@app.get("/post")
def post():
	post_id = request.args.get("post_id", "1").strip() or "1"
	try:
		data = get_post(int(post_id))
		summary = f"投稿ID {data['id']} のデータを取得しました。"
		return render_dashboard(
			active_api="post",
			panel_title="JSONPlaceholder",
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_dashboard(
			active_api="post",
			panel_title="JSONPlaceholder",
			error=str(exc),
		)


@app.get("/joke")
def joke():
	try:
		data = get_joke()
		summary = data["attachments"][0]["text"] if data.get("attachments") else "ダジャレを取得しました。"
		return render_dashboard(
			active_api="joke",
			panel_title="Icanhazdadjoke API",
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_dashboard(
			active_api="joke",
			panel_title="Icanhazdadjoke API",
			error=str(exc),
		)


@app.get("/country")
def country():
	name = request.args.get("name", "Japan").strip() or "Japan"
	try:
		data = get_country(name)
		first = data[0]
		summary = f"{first['name']['common']} の情報を取得しました。"
		return render_dashboard(
			active_api="country",
			panel_title="REST Countries API",
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_dashboard(
			active_api="country",
			panel_title="REST Countries API",
			error=str(exc),
		)


@app.get("/user")
def user():
	try:
		data = get_random_user()
		summary = "ランダムユーザーを取得しました。"
		return render_dashboard(
			active_api="user",
			panel_title="Random User API",
			summary=summary,
			result=data,
			result_json=json.dumps(data, ensure_ascii=False, indent=2),
		)
	except Exception as exc:  # noqa: BLE001
		return render_dashboard(
			active_api="user",
			panel_title="Random User API",
			error=str(exc),
		)


@app.get("/image")
def image():
	width = request.args.get("width", "800").strip() or "800"
	height = request.args.get("height", "500").strip() or "500"
	grayscale = request.args.get("grayscale") == "on"
	blur = request.args.get("blur", "").strip()
	try:
		width_value = max(100, int(width))
		height_value = max(100, int(height))
		blur_value = int(blur) if blur else None
		image_url = get_picsum_url(width_value, height_value, grayscale=grayscale, blur=blur_value)
		summary = f"{width_value} x {height_value} の画像URLを生成しました。"
		result = {
			"width": width_value,
			"height": height_value,
			"grayscale": grayscale,
			"blur": blur_value,
			"url": image_url,
		}
		return render_dashboard(
			active_api="image",
			panel_title="Lorem Picsum",
			summary=summary,
			result=result,
			result_json=json.dumps(result, ensure_ascii=False, indent=2),
			image_url=image_url,
		)
	except Exception as exc:  # noqa: BLE001
		return render_dashboard(
			active_api="image",
			panel_title="Lorem Picsum",
			error=str(exc),
		)


if __name__ == "__main__":
	app.run(host="127.0.0.1", port=5000, debug=True)