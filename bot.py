import logging
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, PeerIdInvalid
import config
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Client("autopayments_userbot", api_id=config.API_ID, api_hash=config.API_HASH, phone_number=config.PHONE_NUMBER)

BOT_ID = 915326936  # ID бота @CardXabarBot
CHANNEL_ID = 2340458063  # ID целевого канала

async def join_channel():
    try:
        chat = await app.join_chat(CHANNEL_ID)
        logger.info(f"Бот присоединился к каналу: {chat.id}")
        return chat.id
    except UserAlreadyParticipant:
        chat = await app.get_chat(CHANNEL_ID)
        logger.info(f"Бот уже является участником канала: {chat.id}")
        return chat.id
    except Exception as e:
        logger.error(f"Не удалось присоединиться к каналу: {e}")
        return None

async def get_peer_id():
    try:
        async for dialog in app.get_dialogs():
            chat_type = dialog.chat.type
            chat_id = dialog.chat.id
            chat_title = dialog.chat.title or dialog.chat.first_name or "Unnamed"
            logger.info(f"Найден диалог: {chat_type} - {chat_id} - {chat_title}")
        return True
    except Exception as e:
        logger.error(f"Ошибка при получении списка диалогов: {e}")
        return False

@app.on_message(filters.bot & filters.user(BOT_ID))
async def forward_to_channel(client, message):
    try:
        await message.forward(CHANNEL_ID)
        logger.info(f"Сообщение переслано: {message.text[:30]}...")
    except FloodWait as e:
        logger.warning(f"Flood wait: sleeping for {e.value} seconds")
        await asyncio.sleep(e.value)
        await message.forward(CHANNEL_ID)
    except Exception as e:
        logger.error(f"Ошибка при пересылке сообщения: {e}")

async def main():
    await app.start()
    logger.info("Userbot запущен. Нажмите Ctrl+C для остановки.")
    
    channel_id = await join_channel()
    if not channel_id:
        logger.error("Не удалось получить ID канала. Завершение работы.")
        return

    # Получаем список всех диалогов
    await get_peer_id()
    
    while True:
        try:
            async for message in app.get_chat_history(channel_id, limit=1):
                if message.text:
                    # Здесь можно добавить дополнительную логику обработки сообщений, если нужно
                    logger.info(f"Получено новое сообщение в канале: {message.text[:30]}...")
                break
        except PeerIdInvalid:
            logger.error(f"Неверный ID канала: {channel_id}. Попытка переподключения.")
            channel_id = await join_channel()
            if not channel_id:
                logger.error("Не удалось переподключиться к каналу. Завершение работы.")
                return
        except Exception as e:
            logger.error(f"Ошибка при получении обновлений: {e}")
        
        await asyncio.sleep(5)  # Проверяем новые сообщения каждые 5 секунд

if __name__ == "__main__":
    app.run(main())