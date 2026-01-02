import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from flask import Flask
from threading import Thread
import json

# Flask app для поддержания работы
app = Flask('')

@app.route('/')
def home():
    return "🤖 Menta Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask, daemon=True)
    t.start()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен бота - ВСТАВЬТЕ СВОЙ ТОКЕН
TOKEN = "8228472308:AAFarC-gKzt3ZTaaafo5-wQLv03zXz6ZKMg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    keyboard = [
        [InlineKeyboardButton("🎫 Получить код проверки", callback_data="get_verify")],
        [InlineKeyboardButton("📱 Получить код регистрации", callback_data="get_register")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = """🚀 *Menta Code Bot*
    
*Создатель:* Г. Марк
*Команда:* NexusMind2026
*Telegram:* t.me/nexusmind20_26

Выберите тип кода:"""
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка кнопок"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "get_verify":
        import random
        import string
        code = "BOT-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        await query.edit_message_text(f"✅ *Код проверки:* `{code}`\n\nДействует 24 часа", parse_mode='Markdown')
    
    elif query.data == "get_register":
        import random
        import string
        code = "REG-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        await query.edit_message_text(f"✅ *Код регистрации:* `{code}`\n\nДействует 7 дней", parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    await update.message.reply_text("Используйте /start для начала работы")

def main():
    """Запуск бота"""
    # Запускаем Flask для поддержания работы
    keep_alive()
    
    # Создаем бота
    app_bot = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CommandHandler("help", help_command))
    app_bot.add_handler(CallbackQueryHandler(handle_button))
    
    # Запускаем
    print("=" * 50)
    print("🤖 Menta Code Bot запущен!")
    print("👨‍💻 Создатель: Г. Марк")
    print("🏢 Команда: NexusMind2026")
    print("📢 Канал: t.me/nexusmind20_26")
    print("=" * 50)
    
    app_bot.run_polling()

if __name__ == "__main__":
    main()