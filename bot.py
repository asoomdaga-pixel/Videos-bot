import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

TOKEN = "9017663390:AAEVI07KWDfza6niiypgPxo8rWn4CfGBTZI"
bot = telebot.TeleBot(TOKEN)

AD_LINK = "https://uplcm.com/4/12196223"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك في بوت تحميل الفيديوهات! 🎥\nأرسل لي أي رابط فيديو وسأقوم بتحميله وإرساله لك فوراً.")

@bot.message_handler(func=lambda message: True)
def handle_video_link(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(message, "الرجاء إرسال رابط صحيح يبدأ بـ http أو https.")
        return

    msg = bot.reply_to(message, "⏳ جاري تحميل الفيديو وإعداده لك...")

    try:
        # إعدادات yt-dlp لتحميل الفيديو
        output_template = 'video.mp4'
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_template,
            'noplaylist': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # إنشاء زر الإعلان الواحد
        markup = InlineKeyboardMarkup()
        ad_button = InlineKeyboardButton("📢 اضغط هنا لدعم البوت ومشاهدة الإعلان", url=AD_LINK)
        markup.add(ad_button)

        # إرسال الفيديو للمستخدم مباشرة مع زر الإعلان كدعم
        with open(output_template, 'rb') as video_file:
            bot.send_video(
                message.chat.id, 
                video_file, 
                caption="✅ إليك الفيديو الخاص بك!\n\n🙏 نرجو دعم استمرار البوت بالضغط على زر الإعلان أعلاه.", 
                reply_markup=markup
            )

        # حذف الملف المؤقت بعد الإرسال
        if os.path.exists(output_template):
            os.remove(output_template)
            
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg.message_id,
            text="❌ حدث خطأ أثناء تحميل الفيديو. تأكد أن الرابط صالح ومتاح."
        )
        if os.path.exists('video.mp4'):
            os.remove('video.mp4')

if __name__ == "__main__":
    bot.infinity_polling()
