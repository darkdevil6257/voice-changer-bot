import os
import requests
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("7983931203:AAE9B5Blt6QFNLyzto-m-NA4rxzhZAnySU8")
VOICEMOD_API_KEY = os.environ.get("controlapi-XuCxcyg1b")

DEFAULT_EFFECT = "woman"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Send me a voice note, I'll convert it to girl voice!")

async def set_effect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        effect = context.args[0]
        context.user_data['effect'] = effect
        await update.message.reply_text(f"✅ Effect set to: {effect}")
    else:
        effects = "woman, robot, alien, baby, deep, echo"
        await update.message.reply_text(f"Available effects:\n{effects}\n\nUsage: /effect woman")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not VOICEMOD_API_KEY:
        await update.message.reply_text("❌ Voicemod API key not configured")
        return
    
    effect = context.user_data.get('effect', DEFAULT_EFFECT)
    
    # Download voice note
    voice_file = await update.message.voice.get_file()
    
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as temp_in:
        await voice_file.download_to_drive(temp_in.name)
        temp_in_path = temp_in.name
    
    # Call Voicemod API (Note: You need actual Voicemod API endpoint)
    # For demo, we'll simulate - but real API requires paid access
    
    await update.message.reply_text(f"🎤 Converting to {effect} voice... (API integration needed)")
    # await update.message.reply_voice(converted_voice)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("effect", set_effect))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()