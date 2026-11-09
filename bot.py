import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

# التوكن الخاص بك الذي زودتني به
TOKEN = "9017663390:AAEVI07KWDfza6niiypgPxo8rWn4CfGBTZI"
bot = telebot.TeleBot(TOKEN)

# رابط الإعلان الجديد النظيف
AD_LINK = "https://uplcm.com/4/12196223"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك في بوت تحميل الفيديوهات! 🎥\nأرسل لي أي رابط فيديو (من يوتيوب، تيك توك، وغيرها) وسأقوم تجهيزه لك فوراً.")

@bot.message_handler(func=lambda message: True)
def handle_video_link(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(message, "الرجاء إرسال رابط صحيح يبدأ بـ http أو https.")
        return

    msg = bot.reply_to(message, "⏳ جاري معالجة الرابط وجلب خيارات التحميل...")

    try:
        # إعدادات yt-dlp لجلب عنوان الفيديو ورابط التحميل المباشر
        ydl_opts = {'format': 'best', 'noplaylist': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            video_title = info.get('title', 'video')

        # إنشاء الأزرار التفاعلية لإجبار المستخدم على التفاعل مع الإعلان أولاً
        markup = InlineKeyboardMarkup()
        
        # زر الإعلان الإجباري بالرابط الجديد النظيف
        ad_button = InlineKeyboardButton("📢 1. اضغط هنا لمشاهدة الإعلان أولاً (مهم)", url=AD_LINK)
        
        # زر التحميل الفعلي الذي يظهر للمستخدم
        download_button = InlineKeyboardButton("📥 2. اضغط هنا لتحميل الفيديو مباشرة", url=video_url)
        
        markup.add(ad_button)
        markup.add(download_button)

        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg.message_id,
            text=f"🎬 **{video_title}**\n\nلتحميل الفيديو، يرجى دعمنا بالضغط على زر الإعلان الأول (1) ثم الضغط على زر التحميل (2):",
            reply_markup=markup,
            parse_mode="Markdown"
        )

    except Exception as e:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg.message_id,
            text="❌ حدث خطأ أثناء جلب الفيديو. تأكد أن الرابط صالح ومتاح للتحميل."
        )

# تشغيل البوت باستمرار
if __name__ == "__main__":
    bot.infinity_polling()
