import os
import requests
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

user_keys = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to UrlCash Bot!\nUse /setapikey to save your API Key.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🛠 Commands:
🔹 /setapikey <your_api_key>
🔹 Paste any link to shorten
🔹 Send multiple links (one per line) for bulk shorten
    """)

async def set_api_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        api_key = context.args[0]
        user_keys[user_id] = api_key
        await update.message.reply_text("✅ API Key saved successfully.")
    except IndexError:
        await update.message.reply_text("❌ Please provide your API key: /setapikey <API_KEY>")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id not in user_keys:
        await update.message.reply_text("⚠️ Use /setapikey first.")
        return

    api_key = user_keys[user_id]
    urls = text.splitlines()
    results = []

    for url in urls:
        response = requests.get(f"https://urlcash.in/api?api={api_key}&url={url}")
        data = response.json()
        if data["status"] == "success":
            results.append(f"🔗 {data['shortenedUrl']}")
        else:
            results.append(f"❌ Failed: {url}")

    await update.message.reply_text("\n".join(results))

# Server to keep alive
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def keep_alive():
    from threading import Thread
    Thread(target=app.run, kwargs={"host": "0.0.0.0", "port": 8080}).start()
