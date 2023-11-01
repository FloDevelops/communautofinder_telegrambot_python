import logging
import json
import re
from os import getenv
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from telegrambot_reservauto.orm import Database

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
TELEGRAM_BOT_TOKEN=getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_WEBHOOK_TOKEN=getenv('TELEGRAM_WEBHOOK_TOKEN')
TELEGRAM_WEBHOOK_URL=getenv('TELEGRAM_WEBHOOK_URL')
TELEGRAM_WEBHOOK_PORT=getenv('TELEGRAM_WEBHOOK_PORT')

database = Database()

WAITLIST = range(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Starts the conversation and check if the user is already in the database. If not, add it'''
    reply_keyboard = [['Yes, keep me updated ✅', 'No, I\'ll chech back myself ❌']]

    # Check if the user is already in the database
    user_data = database.get_user(update.effective_user.id)
    if user_data is None:
        database.create_user(update.effective_user, str(update.effective_chat.id))

        await update.message.reply_text(
            f'Welcome {update.effective_user.first_name}! 🤗\n'
            'I am not quite ready yet, but I will be soon.\n\n'
            'Would you like to join the wailist to receive an invitation when I am ready?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='Yes/No')
        )
        return WAITLIST
    
    else:
        if user_data['is_enabled'] == 1:
            await update.message.reply_text(
                f'Hi {update.effective_user.first_name}!\n'
                'I am ready to help you finding a car rental. 🚗\n\n'
                'Type "/help" to see a list of available commands.'
            )
            return ConversationHandler.END
        
        if user_data['has_accepted_communications'] == 0:
            await update.message.reply_text(
                f'Hi {update.effective_user.first_name}!\n'
                'I am still not quite ready yet.\n\n'
                'Would you like to join the wailist now to receive an invitation when I am ready?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder='Yes/No')
            )
            return WAITLIST

        else:
            await update.message.reply_text(
                f'Hi {update.effective_user.first_name}!\n'
                'I am not quite ready yet, but I will be soon.\n\n'
                'I will send you a message when I am ready.'
            )
            return ConversationHandler.END

    
async def waitlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Adds the user to the waitlist'''
    if update.message.text.lower().startswith('y'):
        database.update_user(update.effective_user, {'has_accepted_communications': 1})
        await update.message.reply_text(
            'I just added you to the waitlist!\n'
            'Turn on your Telegram notifications to see my future message.',
            reply_markup=ReplyKeyboardRemove()
        )

    else:
        await update.message.reply_text('No worries! You can check back here later.',
            reply_markup=ReplyKeyboardRemove()
        )

    return ConversationHandler.END

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

conversations = {
    'registration': ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WAITLIST: [MessageHandler(filters.Regex(re.compile(r'^(y|n)', re.IGNORECASE)), waitlist)]
        },
        fallbacks=[]
    )
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