import ffmpeg

def resize_video(input_file, output_file, width, height):
    """Resizes a video file.

    Args:
        input_file (str): The input video file.
        output_file (str): The output video file.
        width (int): The desired width of the output video.
        height (int): The desired height of the output video.
    """

    stream = ffmpeg.input(input_file)
    stream = stream.resize(width, height)
    stream.output(output_file)

if __name__ == '__main__':
    input_file = 'input.mp4'
    output_file = 'output.mp4'
    width = 1280
    height = 720

    resize_video(input_file, output_file, width, height)



import logging
import logging.config
from pyrogram import Client 
from config import API_ID, API_HASH, BOT_TOKEN, FORCE_SUB, PORT
from aiohttp import web
from plugins.web_support import web_server

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)


class Bot(Client):

    def __init__(self):
        super().__init__(
            name="renamer",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
       await super().start()
       me = await self.get_me()
       self.mention = me.mention
       self.username = me.username 
       self.force_channel = FORCE_SUB
       if FORCE_SUB:
         try:
            link = await self.export_chat_invite_link(FORCE_SUB)                  
            self.invitelink = link
         except Exception as e:
            logging.warning(e)
            logging.warning("Make Sure Bot admin in force sub channel")             
            self.force_channel = None
       app = web.AppRunner(await web_server())
       await app.setup()
       bind_address = "0.0.0.0"
       await web.TCPSite(app, bind_address, PORT).start()
       logging.info(f"{me.first_name} ✅✅ BOT started successfully ✅✅")
      

    async def stop(self, *args):
      await super().stop()      
      logging.info("Bot Stopped 🙄")
        
bot = Bot()
bot.run()
