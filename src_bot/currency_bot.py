from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from currency_service import CurrencyService

class CurrencyBot:
    def __init__(self, token: str):
        self.token = token
        self.application = Application.builder().token(self.token).build()
        self._register_handlers()

    def _register_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CallbackQueryHandler(self.on_currency_selected))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.on_amount_entered))

    def get_keyboard(self):
        buttons = [
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
        return InlineKeyboardMarkup(buttons)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "💰 Конвертер валют для Лизочки❤️\nВыбери направление конвертации:",
            reply_markup=self.get_keyboard()
        )

    async def on_currency_selected(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        pair = query.data
        context.user_data["currency_pair"] = pair
        from_cur, to_cur = pair.split("_")

        rate = CurrencyService.get_rate(pair)

        if rate is None:
            await query.edit_message_text("Ошибка: курс валют не найден.")
            return

        await query.edit_message_text(
            f"Конвертация: {from_cur} → {to_cur}\n"
            f"Текущий курс: 1 {from_cur} = {rate:.4f} {to_cur}\n"
            "Лизочка, введи сумму для конвертации:"
        )

    async def on_amount_entered(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text.replace(",", ".")
        pair = context.user_data.get("currency_pair")

        if not pair:
            await update.message.reply_text("Сначала выбери валюту через /start 🌟")
            return

        try:
            amount = float(text)
            result = CurrencyService.convert(amount, pair)
            from_cur, to_cur = pair.split("_")
            rate = CurrencyService.get_rate(pair)

            await update.message.reply_text(
                f"🔹 {amount:.2f} {from_cur} = {result:.2f} {to_cur}\n"
                f"Курс: 1 {from_cur} = {rate:.4f} {to_cur}\n\n"
                "Для новой конвертации нажми /start"
            )
        except ValueError:
            await update.message.reply_text("Ошибка: введи корректное число. Например: 100 или 50.5")

    def run(self):
        print("Бот запущен и готов к работе...")
        try:
            self.application.run_polling()
        except KeyboardInterrupt:
            print("Бот остановлен вручную.")
