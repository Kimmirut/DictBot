import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from googletrans import Translator

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize translator
translator = Translator()

# File to save translations
DICTIONARY_FILE = 'translations.txt'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Send me an English word and I will translate it to Russian!')

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    word = update.message.text
    try:
        # Translate the word
        translation = translator.translate(word, src='en', dest='ru').text

        # Save the translation to a file
        with open(DICTIONARY_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{word} -> {translation}\n")

        # Send the translation back to the user
        await update.message.reply_text(f'Translation: {translation}')
    except Exception as e:
        logger.error(f"Error translating '{word}': {e}")
        await update.message.reply_text('Sorry, there was an error translating that word.')

async def dict_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        with open(DICTIONARY_FILE, 'r', encoding='utf-8') as f:
            translations = f.readlines()

        if translations:
            response = ''.join(translations)
            await update.message.reply_text(f"Your saved translations:\n{response}")
        else:
            await update.message.reply_text("No translations saved yet.")
    except FileNotFoundError:
        await update.message.reply_text("No translations saved yet.")

async def main() -> None:
    # Your Telegram Bot API token
    TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'

    # Create the Application and pass it your bot's token.
    application = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("dict", dict_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))

    # Start the Bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
