import logging
import os
import asyncio
from flask import Flask, request, jsonify
from telegram import Bot
from telegram.constants import ParseMode

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
PORT = int(os.getenv("PORT", 8000))

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

logging.basicConfig(level=logging.INFO)


def format_message(data):
    return f"""
Новая заявка 🚀

Имя: {data.get('name')}
Услуга: {data.get('title')}
Категория: {data.get('category')}
Город: {data.get('city')}
Цена: {data.get('price')}
Контакт: {data.get('contact')}
Продвижение: {data.get('promo')}

Описание:
{data.get('description')}
"""


@app.route("/")
def home():
    return {"ok": True}


@app.route("/submit-service", methods=["POST"])
def submit():
    data = request.get_json()

    text = format_message(data)

    asyncio.run(
        bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=text
        )
    )

    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
