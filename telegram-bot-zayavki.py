import logging
import os
from typing import Final

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from flask import Flask, request, jsonify

# =========================
# НАСТРОЙКИ
# =========================

BOT_TOKEN: Final[str] = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID: Final[str] = os.getenv("ADMIN_CHAT_ID")
PORT: Final[int] = int(os.getenv("PORT", "8000"))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
telegram_app = None


def format_service_message(data: dict) -> str:
    return (
        "<b>Новая заявка на услугу</b>\n\n"
        f"<b>Имя:</b> {data.get('name')}\n"
        f"<b>Услуга:</b> {data.get('title')}\n"
        f"<b>Категория:</b> {data.get('category')}\n"
        f"<b>Город:</b> {data.get('city')}\n"
        f"<b>Цена:</b> {data.get('price')}\n"
        f"<b>Контакт:</b> {data.get('contact')}\n"
        f"<b>Продвижение:</b> {data.get('promo')}\n\n"
        f"<b>Описание:</b>\n{data.get('description')}"
    )


@app.route("/", methods=["GET"])
def healthcheck():
    return {"ok": True}


@app.route("/submit-service", methods=["POST"])
def submit_service():
    global telegram_app

    try:
        data = request.get_json(force=True)
        message = format_service_message(data)

        import asyncio
        asyncio.run(
            telegram_app.bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=message,
                parse_mode=ParseMode.HTML,
            )
        )

        return jsonify({"ok": True})
    except Exception as e:
        logger.exception("Ошибка")
        return jsonify({"ok": False, "error": str(e)}), 500


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен ✅")


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Твой chat_id: {update.effective_chat.id}")


def main():
    global telegram_app

    telegram_app = Application.builder().token(BOT_TOKEN).build()
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("id", get_id))

    import asyncio

    async def init():
        await telegram_app.initialize()
        await telegram_app.start()

    asyncio.run(init())

    app.run(host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    main()
