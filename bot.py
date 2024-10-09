from pyrogram import Client, filters

# Замените на свои данные
api_id = '20514128'
api_hash = 'dfa79c63ebdae37e0228c004e8973053'
bot_username = '@CardXabarBot'
channel_id = '-1002340458063'

app = Client("my_account", api_id=api_id, api_hash=api_hash)

@app.on_message(filters.user(bot_username))
async def forward_to_channel(client, message):
    await message.forward(channel_id)

app.run()