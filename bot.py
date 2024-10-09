import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

# Настройки
API_ID = "20514128"
API_HASH = "dfa79c63ebdae37e0228c004e8973053"
BOT_ID = 915326936  # ID бота @CardXabarBot
CHANNEL_ID = 2340458063  # ID целевого канала

app = Client("autopayments_userbot", api_id=API_ID, api_hash=API_HASH)

@app.on_message(filters.bot & filters.user(BOT_ID))
async def forward_to_channel(client, message):
    try:
        await message.forward(CHANNEL_ID)
    except FloodWait as e:
        print(f"Flood wait: sleeping for {e.x} seconds")
        await asyncio.sleep(e.x)
        await message.forward(CHANNEL_ID)
    except Exception as e:
        print(f"Error forwarding message: {e}")

async def main():
    await app.start()
    print("Userbot started. Press Ctrl+C to stop.")
    
    # Получение информации о боте и канале
    try:
        bot = await app.get_users(BOT_ID)
        channel = await app.get_chat(CHANNEL_ID)
        print(f"Connected to bot: {bot.first_name}")
        print(f"Target channel: {channel.title}")
    except Exception as e:
        print(f"Error getting chat info: {e}")
    
    # Бесконечный цикл для поддержания работы бота
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    app.run(main())