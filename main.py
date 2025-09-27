import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import BOT_TOKEN, DEVELOPER, SUPPORT_GROUP
from modules.video import download_video
from modules.song import download_song

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Use /song or /video commands.")

async def song_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please provide a song name.")
        return
    filename, data = download_song(query)
    buttons = [
        [InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{DEVELOPER.strip('@')}")],
        [InlineKeyboardButton("🌸 Support Group", url=f"https://t.me/{SUPPORT_GROUP.strip('@')}")],
        [InlineKeyboardButton("▶️ Open in YouTube", url=data["url"])],
    ]
    await update.message.reply_text(
        f"🎵 Title: {data['title']}\n👤 Channel: {data['channel']}\n⏱ Duration: {data['duration']}\n📅 Upload: {data['upload_date']}\n👀 Views: {data['views']}",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await update.message.reply_document(open(filename, "rb"))

async def video_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please provide a video name.")
        return
    filename, data = download_video(query)
    buttons = [
        [InlineKeyboardButton("👨‍💻 Developer", url=f"https://t.me/{DEVELOPER.strip('@')}")],
        [InlineKeyboardButton("🌸 Support Group", url=f"https://t.me/{SUPPORT_GROUP.strip('@')}")],
        [InlineKeyboardButton("▶️ Open in YouTube", url=data["url"])],
    ]
    await update.message.reply_text(
        f"🎬 Title: {data['title']}\n👤 Channel: {data['channel']}\n⏱ Duration: {data['duration']}\n📅 Upload: {data['upload_date']}\n👀 Views: {data['views']}",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await update.message.reply_video(open(filename, "rb"))

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("song", song_command))
    app.add_handler(CommandHandler("video", video_command))
    app.run_polling()
