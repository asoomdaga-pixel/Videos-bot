import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

TOKEN = "9017663390:AAEVI07KWDfza6niiypgPxo8rWn4CfGBTZI"
bot = telebot.TeleBot(TOKEN)

AD_LINK = "https://uplcm.com/4/12196223"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً بك في بوت تحميل الفيديوهات! 🎥\nأرسل لي أي رابط فيديو وسأجهز لك زر الإعلان والتحميل فوراً.")

@bot.message_handler(func=lambda message: True)
def handle_video_link(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(message, "الرجاء إرسال رابط صحيح يبدأ بـ http أو https.")
        return

    # إنشاء الأزرار: زر إجبار المشاهدة أولاً، وزر إتمام التحميل
    markup = InlineKeyboardMarkup()
    
    # زر الإعلان الإجباري
    ad_button = InlineKeyboardButton("📢 اضغط هنا لمشاهدة الإعلان أولاً (مطلوب)", url=AD_LINK)
    
    # زر تأكيد التحميل (نستطيع تمرير الرابط داخل الـ callback_data أو حفظه مؤقتياً)
    # لحل مشكلة حفظ الرابط، سنستخدم طريقة ذكية تعتمد على زر التحميل بعد الإعلان
    # أو جعل زر التحميل يظهر بطلب مباشر
    markup.add(ad_button)
    
    # نخزن رابط الفيديو في الـ callback data لكي يضغط المستخدم عليه بعد الإعلان
    # (ملاحظة: تيليغرام يدعم الـ callback بحدود معينة، لذا سنضع زر التحميل المباشر بعد النقر أو نستخدم طريقة الـ callback الآمنة)
    
    bot.reply_to(
        message, 
        "⏳ **خطوة واحدة تفصلك عن التحميل:**\n\n1️⃣ اضغط على زر الإعلان بالأعلى أولاً.\n2️⃣ بعد الانتهاء من مشاهدة الإعلان، اضغط على زر التحميل أدناه.", 
        reply_markup=markup
    )
    
    # لحفظ الرابط للمستخدم ومعالجته عند الضغط على زر التحميل الفعلي:
    # سنرسل زر ثاني تحتها أو نطلب منه الضغط على زر التحميل
    # دعنا نستخدم زرين مرتبين تنازلياً: (زر الإعلان) ثم (زر جاهز للتحميل)

@bot.message_handler(commands=['getvideo']) # أو طريقة تفاعلية مباشرة
def dummy_handler():
    pass

# كود أبسط وأضمن 100% لتنفيذ فكرتك تماماً (زر واحد يربط العملية):
