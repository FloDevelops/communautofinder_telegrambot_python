import logging
import json
import re
from os import getenv
from dotenv import load_dotenv
# from reservauto import client
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
from telegrambot_reservauto.account import ask_branch, account_conv_handler
from telegrambot_reservauto.orm import Database
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

# reservauto_client = client.ReservautoClient()

database = Database()

SEARCH_TYPE, SEARCH_STATION, SEARCH_STATION_RETURN, SEARCH_STATION_LOCATION, SEARCH_STATION_RADIUS, SEARCH_STATION_RESULTS, SEARCH_FLEX = range(7)

keyboards = {
    'search_type': [['Station', 'Flex']]
}



async def start_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Searches for a car rental'''

    # Check if the user is already in the database
    user_data = database.get_user(update.effective_user.id)
    if user_data is None or user_data['is_enabled'] == 0:
        await update.message.reply_text(
            'Sorry you are still on the wailist and cannot access this feature yet.'
        )
        return ConversationHandler.END
    
    await update.message.reply_text(
        'Are you looking for a car in station or a Flex car?',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboards['search_type'], 
                one_time_keyboard=True, 
                input_field_placeholder='Station/Flex'
                )
    )
    return SEARCH_TYPE


async def check_type_ask_departure_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Routes the user to the correct search function'''

    if update.message.text.lower().startswith('s'):
        await update.message.reply_text(
            'When is your departure date and time? (dd/mm/yyyy hh:mm)',
            reply_markup=ReplyKeyboardRemove()
        )
        return SEARCH_STATION_RETURN    
    
    elif update.message.text.lower().startswith('f'):
        await update.message.reply_text(
            # 'Please send me your location so I can find the closest Flex car.'
            'This feature is not yet available.',
            reply_markup=ReplyKeyboardRemove()
        )
        return SEARCH_FLEX
    
    else:
        await update.message.reply_text(
            'Sorry, I didn\'t understand that. Please try again.',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboards['search_type'], 
                one_time_keyboard=True, 
                input_field_placeholder='Station/Flex'
                )
        )
        return SEARCH_TYPE
    


async def check_departure_ask_return_search_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Asks the user for the return date and time'''

    if re.match(r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$', update.message.text) is None:
        await update.message.reply_text(
            'Sorry, I didn\'t understand that. Please try again.',
        )
        return SEARCH_STATION_RETURN

    await update.message.reply_text(
        'When is your return date and time? (dd/mm/yyyy hh:mm)'
    )
    return SEARCH_STATION_LOCATION


async def check_return_ask_location_search_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Asks the user for the location'''

    if re.match(r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$', update.message.text) is None:
        await update.message.reply_text(
            'Sorry, I didn\'t understand that. Please try again.',
        )
        return SEARCH_STATION_LOCATION

    await update.message.reply_text(
        'Please share the location of the area you want to search in (in location attachment)'
    )
    return SEARCH_STATION_RADIUS


async def check_location_ask_radius_search_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Asks the user for the radius'''

    if update.message.location is None:
        await update.message.reply_text(
            'Sorry, I didn\'t understand that. Please try again.',
        )
        return SEARCH_STATION_RADIUS

    await update.message.reply_text(
        'Please enter the radius of your search area in km (e.g. 0.5, 1, 2)'
    )
    return SEARCH_STATION_RESULTS


async def check_radius_get_results_search_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Shows the results'''

    if re.match(r'^\d{1,2}(\.\d{1,2})?$', update.message.text) is None:
        await update.message.reply_text(
            'Sorry, I didn\'t understand that. Please try again.',
        )
        return SEARCH_STATION_RESULTS

    await update.message.reply_text(
        'Here are the results:'
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
    'search': ConversationHandler(
        entry_points=[CommandHandler('search', start_search)],
        states={
            SEARCH_TYPE: [MessageHandler(filters.Regex(re.compile(r'^(s|f)', re.IGNORECASE)), check_type_ask_departure_search)],
            SEARCH_STATION_RETURN: [MessageHandler(filters.Regex(re.compile(r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$')), check_departure_ask_return_search_station)],
            SEARCH_STATION_LOCATION: [MessageHandler(filters.Regex(re.compile(r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$')), check_return_ask_location_search_station)],
            SEARCH_STATION_RADIUS: [MessageHandler(filters.LOCATION, check_location_ask_radius_search_station)],
            SEARCH_STATION_RESULTS: [MessageHandler(filters.Regex(re.compile(r'^\d{1,2}(\.\d{1,2})?$')), check_radius_get_results_search_station)]
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