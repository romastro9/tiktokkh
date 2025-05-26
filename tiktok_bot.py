import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Replace with your actual token
BOT_TOKEN = "7999290070:AAGQIMmk0Yt2XGJPaymMZ-7nROfFQxFfevY"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("សូមផ្ញើលីងវីដេអូ TikTok មកខ្ញុំ!")

def get_tiktok_download_url(tiktok_url: str):
    api_url = f"https://tikwm.com/api/?url={tiktok_url}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            return data["data"]["play"], data["data"]["title"]
    return None, None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    if "tiktok.com" in message:
        await update.message.reply_text("កំពុងទាញយក... សូមរង់ចាំ")
        video_url, title = get_tiktok_download_url(message)
        if video_url:
            await update.message.reply_video(video=video_url, caption=title)
        else:
            await update.message.reply_text("មិនអាចទាញយកវីដេអូបានទេ។ សូមពិនិត្យលីងម្តងទៀត។")
    else:
        await update.message.reply_text("សូមផ្ញើលីង TikTok ត្រឹមត្រូវ។")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()
