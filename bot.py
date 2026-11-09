import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

# البيانات الخاصة بك
TOKEN = "9017591447:AAGfHfZem368BGl7836cvRRI2hgXfIJdgJg"
ADSTERRA_LINK = "https://auctionr.org/4/2a829ce7c2b25d5fcf74ed829c2b8d0f"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "مرحباً بك في بوت تحميل الفيديوهات! 📥\n\n"
        "أرسل لي رابط الفيديو من أي منصة (يوتيوب، تيك توك، انستغرام) وسأقوم بتحميله لك فوراً."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: message.text and message.text.startswith('http'))
def download_video(message):
    url = message.text.strip()
    processing_msg = bot.reply_to(message, "⏳ جاري معالجة الرابط وتحميل الفيديو...")

    output_template = "video.mp4"
    
    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': output_template,
        'max_filesize': 50 * 1024 * 1024, # 50 ميجا الحد الأقصى للبوت المجاني
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # زر إعلاني يحتوي على رابط Adsterra الخاص بك
        markup = InlineKeyboardMarkup()
        ad_button = InlineKeyboardButton("🔗 اضغط هنا للتحميل السريع والمنتظر", url=ADSTERRA_LINK)
        markup.add(ad_button)

        with open(output_template, 'rb') as video:
            bot.send_video(
                message.chat.id, 
                video, 
                caption="✅ تم تحميل الفيديو بنجاح!\nلا تنسَ دعمنا بالضغط على الزر أدناه.",
                reply_markup=markup
            )
        
        bot.delete_message(message.chat.id, processing_msg.message_id)

    except Exception as e:
        bot.edit_message_text(
            f"❌ حدث خطأ أثناء التحميل: {str(e)}", 
            message.chat.id, 
            processing_msg.message_id
        )
    
    finally:
        if os.path.exists(output_template):
            os.remove(output_template)

if __name__ == "__main__":
    # يمكن رفع هذا السكربت على استضافة مجانية تعمل بـ Webhook دون الحاجة لاتصال هاتفك بالإنترنت
    print("البوت جاهز ومربوط برابط Adsterra!")
    bot.infinity_polling()
