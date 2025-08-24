import os
from telegram.ext import Application, CommandHandler, ChatMemberHandler
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

welcome_enabled = False
bye_enabled = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I'm KiraFix💡Community's happy welcome bot. I'll greet new members when they join our communiy! \n\n"
        "👋🏾❤️👨🏾‍💻 KiraFix💡Channel (https://t.me/KiraFix_tech) 🙏🏾❤️👩🏾‍💻 \n\n"
        "👋🏾❤️👨🏾‍💻 KiraFix💡Community (https://t.me/KiraFix_tech_discussion) 🙏🏾❤️👩🏾‍💻 \n\n"
        "You can use /startwelcome and /stopwelcome to control welcome messages, and /startbye and /stopbye for goodbye messages.\n"
        "Proudly made with love in Ethiopia 🇪🇹❤️"
    )

async def startwelcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global welcome_enabled
    welcome_enabled = True
    await update.message.reply_text(
        "Welcome messages have been enabled!🍀 \n\n" 
        "I'll now greet new members when they join.😊"
        )

async def stopwelcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global welcome_enabled
    welcome_enabled = False
    await update.message.reply_text(
    "Welcome messages have been disabled.🙅🏾‍♂️🙅🏾‍♀️ \n\n" 
    "I won't greet new members for now.😴")

async def startbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bye_enabled
    bye_enabled = True
    await update.message.reply_text("Goodbye messages have been enabled!💁🏾‍♂️ \n\n " 
    "I'll now say goodbye to members who leave.😢")

async def stopbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global bye_enabled
    bye_enabled = False
    await update.message.reply_text(
    "Goodbye messages have been disabled.🙅🏾‍♂️🙅🏾‍♀️ \n " 
    "I won't send farewell messages for now.😴") 

async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not welcome_enabled:
        return
    chat_member = update.chat_member
    if chat_member.new_chat_member.status == "member" and chat_member.new_chat_member.user.id != context.bot.id:
        first_name = chat_member.new_chat_member.user.first_name
        last_name = chat_member.new_chat_member.user.last_name or ""
        welcome_message = (
                f"Hello {first_name} {last_name} 👋🏾 \n welcome to our awesome community which you are a part of now!  👨🏾‍💻👩🏾‍💻🚀 \n\n"
                "We're happy to have you here! Since we are on the same team, feel free to introduce yourself, join the conversation and grow with us. 📈😊 \n\n"
                "We believe your presence will be a blessing to the community. 🙏🏾 \n\n"
                "@KiraFix_tech_discussion"
        )
        await context.bot.send_message(chat_id=chat_member.chat.id, text=welcome_message)

async def goodbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bye_enabled:
        return
    chat_member = update.chat_member
    if (
        chat_member.old_chat_member.status in ["member", "administrator", "creator"] 
        and chat_member.new_chat_member.status == "left"
    ):
        first_name = chat_member.from_user.first_name
        last_name = chat_member.from_user.last_name or ""
        goodbye_message = (
            f"Goodbye {first_name} {last_name} 😢 \n we're sad to see you leave our community. \n\n"
            "We wish you all the best! 🙏🏾 and We are going to miss you 🥺🥺 \n\n" 
            "You're always welcome back at KiraFix💡Community! ❤️ \n\n"
            "@KiraFix_tech_discussion"
        )
        await context.bot.send_message(chat_id=update.chat_member.chat.id, text=goodbye_message)

async def error_handler(update, context):
        print(f"Error: {context.error}")
        if isinstance(context.error, TelegramError):
            print(f"Telegram API error: {context.error.message}")

def main():
    token = os.getenv("BOT_TOKEN")
    if not token: 
        raise ValueError("BOT_TOKEN not set in environment variables")
    
    application = Application.builder().token(token).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("startwelcome", startwelcome))
    application.add_handler(CommandHandler("stopwelcome", stopwelcome))
    application.add_handler(CommandHandler("startbye", startbye))
    application.add_handler(CommandHandler("stopbye", stopbye))

    
    application.add_handler(ChatMemberHandler(welcome, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(ChatMemberHandler(goodbye, ChatMemberHandler.CHAT_MEMBER))

    application.add_handler(error_handler)
    print("Bot is running...")
    application.run_polling (
        allowed_updates=["chat_member"],
        drop_pending_updates=True,
        timeout=30
    )

if __name__ == '__main__':
    main()
