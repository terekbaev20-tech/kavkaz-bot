import os
import logging
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
PORT = int(os.getenv("PORT", 8000))

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)


def format_message(data: dict) -> str:
    return (
        "Новая заявка 🚀\n\n"
        f"Имя: {data.get('name', '-')}\n"
        f"Услуга: {data.get('title', '-')}\n"
        f"Категория: {data.get('category', '-')}\n"
        f"Город: {data.get('city', '-')}\n"
        f"Цена: {data.get('price', '-')}\n"
        f"Контакт: {data.get('contact', '-')}\n"
        f"Продвижение: {data.get('promo', '-')}\n\n"
        f"Описание:\n{data.get('description', '-')}"
    )


@app.route("/", methods=["GET"])
def home():
    return {"ok": True}


@app.route("/submit-service", methods=["POST"])
def submit_service():
    try:
        data = request.get_json(force=True)
        text = format_message(data)

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        response = requests.post(
            url,
            json={
                "chat_id": ADMIN_CHAT_ID,
                "text": text,
            },
            timeout=15,
        )

        result = response.json()

        if not response.ok or not result.get("ok"):
            return jsonify({"ok": False, "error": result}), 500

        return jsonify({"ok": True}), 200

    except Exception as e:
        logging.exception("Ошибка при отправке заявки")
        return jsonify({"ok": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
