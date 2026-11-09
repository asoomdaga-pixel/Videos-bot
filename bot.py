import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

TOKEN = "9017663390:AAEVI07KWDfza6niiypgPxo8rWn4CfGBTZI"
bot = telebot.TeleBot(TOKEN)

AD_LINK = "https://uplcm.com/4/12196223"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك في بوت تحميل الفيديوهات! 🎥\nأرسل لي أي رابط فيديو (تيك توك، يوتيوب، إلخ) وسأقوم بتحميله وإرساله لك فوراً.")

@bot.message_handler(func=lambda message: True)
def handle_video_link(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(message, "الرجاء إرسال رابط صحيح يبدأ بـ http أو https.")
        return

    # رسالة تنبيه أولية للمستخدم
    msg = bot.reply_to(message, "⏳ جارِ الاتصال بالسيرفر ومعالجة الرابط...")

    try:
        # إعدادات yt-dlp للتحميل المؤقت
        output_template = 'video.mp4'
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_template,
            'noplaylist': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # إنشاء زر الإعلان الإجباري
        markup = InlineKeyboardMarkup()
        ad_button = InlineKeyboardButton("📢 1. اضغط هنا لمشاهدة الإعلان أولاً (مهم)", url=AD_LINK)
        markup.add(ad_button)

        # التحقق من وجود الملف المرسل وإرساله
        if os.path.exists(output_template):
            with open(output_template, 'rb') as video_file:
                bot.send_video(
                    message.chat.id, 
                    video_file, 
                    caption="✅ تم تحميل الفيديو بنجاح!\n\n🙏 نرجو دعم استمرار البوت بالضغط على زر الإعلان أعلاه.", 
                    reply_markup=markup
                )
            # حذف الملف المؤقت من السيرفر
            os.remove(output_template)
        else:
            bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=msg.message_id,
                text="❌ تعذر العثور على ملف الفيديو بعد التحميل."
            )
            return

        # حذف رسالة الانتظار
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        # في حال حدوث أي خطأ، سيخبرك البوت به بدلاً من الصمت
        error_message = str(e)
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=msg.message_id,
            text=f"❌ حدث خطأ أثناء جلب الفيديو:\n`{error_message[:100]}`\n\nتأكد أن الرابط صالح ومتاح للعامة.",
            parse_mode="Markdown"
        )
        if os.path.exists('video.mp4'):
            os.remove('video.mp4')

if __name__ == "__main__":
    bot.infinity_polling()
