import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import yt_dlp

TOKEN = "9017663390:AAEVI07KWDfza6niiypgPxo8rWn4CfGBTZI"
bot = telebot.TeleBot(TOKEN)

AD_LINK = "https://uplcm.com/4/12196223"

# قاموس مؤقت لحفظ روابط المستخدمين
user_links = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك في بوت تحميل الفيديوهات! 🎥\nأرسل لي أي رابط فيديو وسأعطيك خيارات المشاهدة والتحميل.")

@bot.message_handler(func=lambda message: True)
def handle_video_link(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(message, "الرجاء إرسال رابط صحيح يبدأ بـ http أو https.")
        return

    # حفظ الرابط مؤقتاً لهذا المستخدم
    user_links[message.chat.id] = url

    # إنشاء الأزرار: زر الإعلان الإجباري أولاً، وتحته زر تحميل الفيديو الذي لا يعمل إلا بعد الإعلان
    markup = InlineKeyboardMarkup()
    ad_button = InlineKeyboardButton("📢 1. اضغط هنا لمشاهدة الإعلان أولاً (مطلوب)", url=AD_LINK)
    ready_button = InlineKeyboardButton("📥 2. اضغط هنا لتحميل الفيديو بعد مشاهدة الإعلان", callback_data="download_now")
    
    markup.add(ad_button)
    markup.add(ready_button)

    bot.reply_to(
        message, 
        "🎬 **تم استلام الرابط بنجاح!**\n\nلتحميل الفيديو، يرجى اتباع الخطوتين:\n1️⃣ اضغط على زر الإعلان (1) بالأعلى.\n2️⃣ بعد الانتهاء، اضغط على زر التحميل (2) أدناه.", 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "download_now")
def callback_download(call):
    chat_id = call.message.chat.id
    
    if chat_id not in user_links:
        bot.answer_callback_query(call.id, "انتهت صلاحية الجلسة، أرسل الرابط من جديد.", show_alert=True)
        return

    url = user_links[chat_id]
    
    # تعديل الرسالة لإخبار المستخدم بأن البوت يبدأ التحميل
    bot.edit_message_text(
        chat_id=chat_id,
        message_id=call.message.message_id,
        text="⏳ جاري تحميل الفيديو وإرساله لك الآن..."
    )

    try:
        output_template = 'video.mp4'
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_template,
            'noplaylist': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.exists(output_template):
            with open(output_template, 'rb') as video_file:
                bot.send_video(chat_id, video_file, caption="✅ تفضل فيديو الخاص بك!")
            os.remove(output_template)
        
        # حذف رسالة الانتظار
        bot.delete_message(chat_id, call.message.message_id)
        
        # مسح الرابط المؤقت
        del user_links[chat_id]

    except Exception as e:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text="❌ حدث خطأ أثناء تحميل الفيديو. تأكد أن الرابط صالح ومتاح."
        )
        if os.path.exists('video.mp4'):
            os.remove('video.mp4')

if __name__ == "__main__":
    bot.infinity_polling()
