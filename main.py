#!/usr/bin/env python3
"""
🤖 Menta Telegram Bot - Упрощенная рабочая версия для Render
"""

import os
import sys
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import random
import string

# ========== НАСТРОЙКА ЛОГИРОВАНИЯ ==========
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========== ТОКЕН БОТА ==========
TOKEN = "8228472308:AAFarC-gKzt3ZTaaafo5-wQLv03zXz6ZKMg"

# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========
def generate_code(prefix="BOT"):
    """Генерирует случайный код"""
    chars = string.ascii_uppercase + string.digits
    code = f"{prefix}-{''.join(random.choices(chars, k=6))}"
    return code

# ========== КОМАНДЫ БОТА ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    
    keyboard = [
        [InlineKeyboardButton("🎫 Получить код проверки", callback_data="verify")],
        [InlineKeyboardButton("📱 Получить код регистрации", callback_data="register")],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data="help")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = f"""
    🚀 *Привет, {user.first_name}!*
    
    🤖 *Menta Code Bot* - выдача кодов
    
    👨‍💻 *Создатель:* Г. Марк
    🏢 *Команда:* NexusMind2026
    📢 *Канал:* @nexusmind20_26
    
    Выберите нужное действие:
    """
    
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий кнопок"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    
    if query.data == "verify":
        code = generate_code("BOT")
        response = f"""
        ✅ *Код проверки сгенерирован!*
        
        📝 *Код:* `{code}`
        👤 *Для:* {user.first_name}
        ⏰ *Срок:* 24 часа
        🎯 *Назначение:* Проверка работы ботов
        
        🏢 *NexusMind2026*
        """
        await query.edit_message_text(response, parse_mode='Markdown')
    
    elif query.data == "register":
        code = generate_code("REG")
        response = f"""
        ✅ *Код регистрации сгенерирован!*
        
        📝 *Код:* `{code}`
        👤 *Для:* {user.first_name}
        ⏰ *Срок:* 7 дней
        🎯 *Назначение:* Регистрация в Menta
        
        🏢 *NexusMind2026*
        """
        await query.edit_message_text(response, parse_mode='Markdown')
    
    elif query.data == "help":
        help_text = """
        ℹ️ *Помощь по боту*
        
        *Как использовать:*
        1. Нажмите "🎫 Получить код проверки" для тестирования
        2. Нажмите "📱 Получить код регистрации" для приложения
        
        *Информация:*
        • Создатель: Г. Марк
        • Команда: NexusMind2026
        • Канал: @nexusmind20_26
        
        *Техподдержка:*
        По всем вопросам: @nexusmind20_26
        """
        await query.edit_message_text(help_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    await update.message.reply_text("Используйте /start для начала работы")

# ========== ОСНОВНАЯ ФУНКЦИЯ ==========
def main():
    """Запуск бота"""
    print("=" * 50)
    print("🚀 Запуск Menta Code Bot...")
    print(f"👨‍💻 Создатель: Г. Марк")
    print(f"🏢 Команда: NexusMind2026")
    print(f"📢 Канал: @nexusmind20_26")
    print("=" * 50)
    
    try:
        # Создаем приложение бота
        application = Application.builder().token(TOKEN).build()
        
        # Регистрируем обработчики
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CallbackQueryHandler(button_handler))
        
        # Запускаем бота
        print("✅ Бот успешно инициализирован")
        print("⏳ Запуск polling...")
        
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"❌ Ошибка при запуске: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
