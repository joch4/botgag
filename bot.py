import discord
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import threading

import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

subscribers = set()  # подписчики Telegram

# --- Telegram Bot ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    subscribers.add(user_id)
    await update.message.reply_text("✅ Ты подписан на уведомления о рестоке!")

async def send_to_subscribers(text):
    for user_id in subscribers:
        try:
            await telegram_bot.send_message(chat_id=user_id, text=text)
        except Exception as e:
            print(f"❌ Не удалось отправить {user_id}: {e}")

telegram_app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
telegram_bot = Bot(token=TELEGRAM_TOKEN)
telegram_app.add_handler(CommandHandler("start", start))

# --- Discord Bot ---
class MyDiscordClient(discord.Client):
    async def on_ready(self):
        print(f'✅ Discord бот вошёл как {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        text = f"[{message.channel.name}] {message.author.name}: {message.content}"
        await send_to_subscribers(text)

discord_client = MyDiscordClient(intents=discord.Intents.all())

# --- Запуск обоих ботов ---
def run_discord():
    discord_client.run(DISCORD_TOKEN)

def run_telegram():
    telegram_app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_discord).start()
    run_telegram()
