import asyncio
import telegram

TOKEN = "6752231619:AAFxmtm-YvdwlMCQAkRraKuGllvcui9JGx4"
chat_id = 1476474149
# bot = telegram.Bot(token=TOKEN)

class TelegramBot():
    def __init__(self, token):
        self.token = token
    def guiTinNhan(self, chat_id, text:str):
        async def send_message():
            bot = telegram.Bot(token=self.token)
            await bot.send_message(chat_id, text=text)
        asyncio.run(send_message())
    def guiAnh(self, chat_id, photo, caption):
        async def send_message():
            bot = telegram.Bot(token=self.token)
            await bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)
        asyncio.run(send_message())
# bot = TelegramBot(token=TOKEN)
# bot.guiTinNhan(chat_id=chat_id, text="Hello")

# bot.guiAnh(chat_id=chat_id, photo=open('TBT_resize.png', 'rb'), caption="TBT kính mến")