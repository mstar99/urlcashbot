import os
from bot import start, help_command, set_api_key, handle_message
from keep_alive import keep_alive
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

keep_alive()

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("setapikey", set_api_key))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

print("Bot started...")
app.run_polling()
