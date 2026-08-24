import telebot

# ضع التوكن الخاص بك هنا
TOKEN = "8719764667:AAH-VYsnfmGFphGlhoBFGlPn06tWPndvVi4"
bot = telebot.TeleBot(TOKEN)

print("--- البوت الآن في وضع الاستماع ---")
print("اذهب إلى تليجرام وأرسل كلمة 'Hi' للبوت...")

@bot.message_handler(func=lambda message: True)
def get_id(message):
    print(f"\n✅ تم استلام رسالة!")
    print(f"الـ Chat ID الخاص بك هو: {message.chat.id}")
    print("انسخ هذا الرقم واحفظه، هذا هو عنوانك الذي سنستخدمه!")

# هذا السطر يجعل البرنامج مستمراً في العمل
bot.infinity_polling()