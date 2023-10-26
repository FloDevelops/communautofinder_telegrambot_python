import logging
import json
from os import getenv
from dotenv import load_dotenv
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=
f'''Hi {update.effective_user.first_name}!

I interact with Reservauto / Communauto to help you finding a car rental by checking for car availabilities.

Type "/help" to see a list of available commands.'''
        )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=update.message.text
        )

async def get_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Available commands:\n' + '\n'.join([f'/{command[0]} - {command[1]["description"]}' for command in commands.items()])
        )

async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=json.dumps(update.to_dict(), indent=4)
        )

commands = {
    'start': {
        'description': 'Start the bot',
        'function': start
    },
    'echo': {
        'description': 'Echo the message',
        'function': echo
    },
    'help': {
        'description': 'Show help',
        'function': get_help
    },
    'debug': {
        'description': 'Show debug info',
        'function': debug
    }
}

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    for command in commands.items():
        application.add_handler(CommandHandler(command[0], command[1]['function']))
        
    application.run_webhook(
        listen='127.0.0.1',
        port=TELEGRAM_WEBHOOK_PORT,
        secret_token=TELEGRAM_WEBHOOK_TOKEN,
        webhook_url=f'{TELEGRAM_WEBHOOK_URL}'
    )

if __name__ == '__main__':
    main()