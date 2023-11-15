import logging
import json
from os import getenv
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from telegrambot_reservauto.account import ask_branch, account_conv_handler
from telegrambot_reservauto.search_station import start_search, search_station_conv_handler
from telegrambot_reservauto.welcome import start, start_conv_handler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
TELEGRAM_BOT_TOKEN=getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_WEBHOOK_TOKEN=getenv('TELEGRAM_WEBHOOK_TOKEN')
TELEGRAM_WEBHOOK_URL=getenv('TELEGRAM_WEBHOOK_URL')
TELEGRAM_WEBHOOK_PORT=getenv('TELEGRAM_WEBHOOK_PORT')



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
    'help': {
        'description': 'Show help',
        'function': get_help
    },
    'account': {
        'description': 'Manage your account',
        'function': ask_branch
    },
    'search': {
        'description': 'Search for a car rental',
        'function': start_search
    },
    'echo': {
        'description': 'Echo the message',
        'function': echo
    },
    'debug': {
        'description': 'Show debug info',
        'function': debug
    }
}

conversations = {
    'registration': start_conv_handler(),
    'account': account_conv_handler(),
    'search': search_station_conv_handler()
}

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    for handler in conversations.items():
        application.add_handler(handler[1])

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