from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

RATES = {
    "USD_RUB": 80.33,  # 1 USD = 90.50 RUB
    "RUB_USD": 1 / 80.33,  # 1 RUB = 0.01105 USD
    "THB_RUB": 2.45,  # 1 THB = 2.45 RUB
    "RUB_THB": 1 / 2.45,  # 1 RUB = 0.4082 THB
    "USD_THB": 32.48,  # 1 USD = 36.80 THB
    "THB_USD": 1 / 32.48  # 1 THB = 0.02717 USD
}


def get_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("USD → RUB", callback_data="USD_RUB"),
            InlineKeyboardButton("RUB → USD", callback_data="RUB_USD")
        ],
        [
            InlineKeyboardButton("THB → RUB", callback_data="THB_RUB"),
            InlineKeyboardButton("RUB → THB", callback_data="RUB_THB")
        ],
        [
            InlineKeyboardButton("USD → THB", callback_data="USD_THB"),
            InlineKeyboardButton("THB → USD", callback_data="THB_USD")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💰 Конвертер валют для Лизочки❤️\nВыбери направление конвертации:",
        reply_markup=get_keyboard()
    )


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Сохраняем выбранную пару и показываем пользователю
    pair = query.data
    context.user_data["currency_pair"] = pair
    from_cur, to_cur = pair.split("_")

    await query.edit_message_text(
        f"Конвертация: {from_cur} → {to_cur}\n"
        f"Текущий курс: 1 {from_cur} = {RATES[pair]:.4f} {to_cur}\n"
        "Лизочка, введи сумму для конвертации:"
    )


async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        amount = float(update.message.text.replace(",", "."))
        pair = context.user_data.get("currency_pair")

        if not pair:
            await update.message.reply_text("Солнце, сначала выбери валюту (/start)")
            return

        if pair not in RATES:
            await update.message.reply_text("Ошибка: курс не найден")
            return

        from_cur, to_cur = pair.split("_")
        result = amount * RATES[pair]

        await update.message.reply_text(
            f"🔹 {amount:.2f} {from_cur} = {result:.2f} {to_cur}\n"
            f"Курс: 1 {from_cur} = {RATES[pair]:.4f} {to_cur}\n\n"
            "Новая конвертация: /start"
        )

    except ValueError:
        await update.message.reply_text("Ошибка: введи число! Например: 100 или 50.5")


def main():
    application = Application.builder().token("").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert))

    print("Бот запущен и готов к работе...")
    application.run_polling()


if __name__ == "__main__":
    main()