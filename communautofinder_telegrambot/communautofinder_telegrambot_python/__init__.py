from os import getenv
from dotenv import load_dotenv
import asyncio, logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

load_dotenv()
TELEGRAM_BOT_TOKEN=getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_WEBHOOK_TOKEN=getenv('TELEGRAM_WEBHOOK_TOKEN')
TELEGRAM_WEBHOOK_URL=getenv('TELEGRAM_WEBHOOK_URL')
TELEGRAM_WEBHOOK_PORT=getenv('TELEGRAM_WEBHOOK_PORT')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

commands = [
    {
        'command': 'start',
        'description': 'Start the bot'
    },
    {
        'command': 'echo',
        'description': 'Echo the message'
    },
    {
        'command': 'help',
        'description': 'Show help'
    }
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text='Available commands:\n' + '\n'.join([f'/{command["command"]} - {command["description"]}' for command in commands]))

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    echo_handler = CommandHandler('echo', echo)
    application.add_handler(echo_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)
    
    # application.run_polling()
    application.run_webhook(
        listen='127.0.0.1',
        port=TELEGRAM_WEBHOOK_PORT,
        secret_token=TELEGRAM_WEBHOOK_TOKEN,
        webhook_url=f'{TELEGRAM_WEBHOOK_URL}'
    )
