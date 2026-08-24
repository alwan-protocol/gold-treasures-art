import telebot

# ضع التوكن الخاص بك هنا بين علامات التنصيص
TOKEN = "8719764667:AAH-VYsnfmGFphGlhoBFGlPn06tWPndvVi4"
bot = telebot.TeleBot(TOKEN)
print("--- البوت في وضع الاستماع ---")

@bot.message_handler(func=lambda message: True)
def get_id(message):
    print(f"\n✅ تم استلام رسالة!")
    print(f"الـ Chat ID الخاص بك هو: {message.chat.id}")

bot.infinity_polling()