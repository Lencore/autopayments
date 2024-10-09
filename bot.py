import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, PeerIdInvalid

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
        print(f"Message forwarded: {message.text[:30]}...")
    except FloodWait as e:
        print(f"Flood wait: sleeping for {e.value} seconds")
        await asyncio.sleep(e.value)
        await message.forward(CHANNEL_ID)
    except Exception as e:
        print(f"Error forwarding message: {e}")

async def get_chat_info(client, chat_id):
    for _ in range(5):  # Попробуем 5 раз
        try:
            return await client.get_chat(chat_id)
        except PeerIdInvalid:
            print(f"Peer ID {chat_id} is invalid. Waiting before retry...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error getting chat info for {chat_id}: {e}")
            await asyncio.sleep(5)
    return None

async def main():
    await app.start()
    print("Userbot started. Press Ctrl+C to stop.")
    
    # Получение информации о боте и канале
    bot = await get_chat_info(app, BOT_ID)
    channel = await get_chat_info(app, CHANNEL_ID)
    
    if bot:
        print(f"Connected to bot: {bot.first_name}")
    else:
        print("Failed to get bot info. Please check the BOT_ID.")
    
    if channel:
        print(f"Target channel: {channel.title}")
    else:
        print("Failed to get channel info. Please check the CHANNEL_ID.")
    
    # Бесконечный цикл для поддержания работы бота
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    app.run(main())