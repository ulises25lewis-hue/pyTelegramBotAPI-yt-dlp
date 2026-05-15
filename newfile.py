import os
import telebot
from yt_dlp import YoutubeDL

# التوكن الخاص بك جاهز ومربوط
BOT_TOKEN = "8711733345:AAFxCYJtbf8aed4X4CTTAeeonNo6gQZMGOM"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "📥 **مرحباً بك في بوت التحميل الشامل!**\n\n"
        "أرسل لي أي رابط فيديو من يوتيوب، فيسبوك، تيك توك، أو إنستجرام وسأقوم بتحميله فوراً.\n\n"
        "---\n"
        "👨‍💻 **المطور:** أحمد السيد"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_links(message):
    url = message.text.strip()
    
    if not (url.startswith("http://") or url.startswith("https://")):
        bot.reply_to(message, "⚠️ من فضلك أرسل رابطاً صحيحاً يبدأ بـ https://")
        return

    status_msg = bot.reply_to(message, "⏳ جاري فحص الرابط وتحميل الفيديو، يرجى الانتظار...")

    filename = "phone_download.mp4"

    ydl_opts = {
        'format': 'best[ext=mp4][filesize<50M]/best[filesize<50M]/best',
        'outtmpl': 'phone_download.%(ext)s', 
        'quiet': True,                          
        'no_warnings': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_file = ydl.prepare_filename(info)
            
            if os.path.exists(downloaded_file):
                filename = downloaded_file
            elif os.path.exists(os.path.splitext(downloaded_file)[0] + ".mp4"):
                filename = os.path.splitext(downloaded_file)[0] + ".mp4"

            if os.path.exists(filename):
                bot.edit_message_text("📤 جاري رفع الفيديو الآن إلى تيليجرام...", chat_id=message.chat.id, message_id=status_msg.message_id)
                
                with open(filename, 'rb') as video_file:
                    bot.send_video(
                        chat_id=message.chat.id,
                        video=video_file,
                        caption="✅ **تم التحميل بنجاح!**\n\n👨‍💻 **المطور:** أحمد السيد",
                        supports_streaming=True,
                        parse_mode="Markdown"
                    )
                
                bot.delete_message(message.chat.id, status_msg.message_id)
            else:
                bot.edit_message_text("❌ لم يتم العثور على الملف بعد تحميله.", chat_id=message.chat.id, message_id=status_msg.message_
