import os, youtube_dl, requests, time
from config import Config
from youtube_search import YoutubeSearch
from pyrogram.handlers import MessageHandler
from pyrogram import Client, filters
import yt_dlp
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)


#config#

bot = Client(
    'moonBot',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

#start mesajı

@bot.on_message(filters.command("alive") & filters.user(Config.BOT_OWNER))
async def live(client: Client, message: Message):
    livemsg = await message.reply_text('`EGOİSTBEY Hoşgeldin KraL Bende Burdayım🥳 **BİRİCİK SAHİBİM @DeepKraL 🖤`')
    
#musik indirme#

@bot.on_message(filters.command("bul") & ~filters.edited)
def bul(_, message):
    query = " ".join(message.command[1:])
    m = message.reply("<b>• 🔍 𝐀𝐑𝐀𝐍𝐈𝐘𝐎𝐑...</b>")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        m.edit("<b>⛔ **❌ Ş𝚊𝚛𝚔ı 𝙱𝚞𝚕𝚞𝚗𝚊𝚖𝚊𝚍ı.\n\n 𝙻𝚄̈𝚃𝙵𝙴𝙽 𝙶𝙴𝙲̧𝙴𝚁𝙻𝙸̇ 𝙱𝙸̇𝚁 𝚂̧𝙰𝚁𝙺𝙸 𝙰𝙳𝙸 𝚅𝙴𝚁𝙸̇𝙽.**</b>")
        print(str(e))
        return
    m.edit("<b>•> 📥 𝙸̇𝙽𝙳𝙸̇𝚁𝙼𝙴 𝙸̇𝚂̧𝙻𝙴𝙼𝙸̇ 𝙱𝙰𝚂̧𝙻𝙰𝚃𝙸𝙻𝙳𝙸...**</b>")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"🎶 𝐈̇𝐍𝐃𝐈̇𝐑𝐈̇𝐋𝐃𝐈̇ 🎶\n\n**İndirdiğiniz Tüm Müzikler Ve Daha Fazlası @YoutubeVcMuzik Kanalımızda."
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("•> **Yükleniyor**...")
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name, performer="👇👇👇👇👇👇👇👇")
        m.delete()
        bot.send_audio(chat_id=Config.PLAYLIST_ID, audio=audio_file, caption=rep, performer="@SohbetMis", parse_mode='md', title=title, duration=dur, thumb=thumb_name)
    except Exception as e:
        m.edit("<b>⛔ **Hatanın düzelmesini bekleyin** .</b>")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()
