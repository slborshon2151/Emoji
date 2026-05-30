import telebot
from telebot.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# আপনার BotFather থেকে পাওয়া টোকেন এখানে বসান
API_TOKEN = '8421975039:AAELOhF4ojPT-xceU2QDqMGoC6N-PMY8myQ'
bot = telebot.TeleBot(API_TOKEN)

# স্টার্ট কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    
    # আপনার Vercel/GitHub Pages লিঙ্কটি এখানে বসাবেন
    WEB_APP_URL = "https://your-emoji-webapp.vercel.app"
    
    web_app = WebAppInfo(url=WEB_APP_URL)
    button = KeyboardButton(text="🚀 Open Emoji Workspace", web_app=web_app)
    markup.add(button)
    
    welcome_msg = (
        "👋 *Welcome to Premium Emoji Post Creator!*\n\n"
        "নিচের বাটনে ক্লিক করে আপনার কাস্টম অ্যানিমেটেড ইমোজি পোস্ট তৈরি করুন।"
    )
    bot.send_message(message.chat.id, welcome_msg, parse_mode="Markdown", reply_markup=markup)

# ওয়েব অ্যাপ থেকে ডাটা রিসিভ করার হ্যান্ডলার
@bot.message_handler(content_types=['web_app_data'])
def handle_web_app_data(message):
    formatted_post = message.web_app_data.data # <tg-emoji> সহ কোড আসবে এখানে
    
    bot.send_message(message.chat.id, "🎯 *Your Post Preview:*", parse_mode="Markdown")
    
    # এটি সরাসরি অ্যানিমেটেড ইমোজি সহ মেসেজটি শো করাবে চ্যাটে
    bot.send_message(message.chat.id, formatted_post, parse_mode="HTML")
    
    # দ্রুত শেয়ার বা চ্যানেলে নেওয়ার জন্য ইনলাইন বাটন
    markup = InlineKeyboardMarkup()
    share_button = InlineKeyboardButton(text="📢 Share via Inline", switch_inline_query=formatted_post)
    markup.add(share_button)
    
    bot.send_message(
        message.chat.id, 
        "👆 উপরের মেসেজটি ফরওয়ার্ড করে আপনার চ্যানেলে নিতে পারেন। অথবা সরাসরি ইনলাইনে শেয়ার করতে নিচের বাটনটি ব্যবহার করুন:", 
        reply_markup=markup
    )

# ইনলাইন কুয়েরি সাপোর্ট (যাতে বাটন ক্লিক করে শেয়ার করা যায়)
@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(inline_query):
    try:
        input_text = inline_query.query
        result = telebot.types.InlineQueryResultArticle(
            id='1',
            title="Click here to send the post",
            description=input_text[:50] + "...",
            input_message_content=telebot.types.InputTextMessageContent(
                message_text=input_text,
                parse_mode="HTML"
            )
        )
        bot.answer_inline_query(inline_query.id, [result])
    except Exception as e:
        print(f"Inline Error: {e}")

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
    