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
    filters
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

WAITLIST, SEARCH_TYPE, SEARCH_STATION, SEARCH_STATION_RETURN, SEARCH_STATION_LOCATION, SEARCH_STATION_RADIUS, SEARCH_STATION_RESULTS, SEARCH_FLEX = range(8)

keyboards = {
    'waitlist': [['Yes, keep me updated ✅', 'No, I\'ll chech back myself ❌']],
    'search_type': [['Station', 'Flex']]
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Starts the conversation and check if the user is already in the database. If not, add it'''

    # Check if the user is already in the database
    user_data = database.get_user(update.effective_user.id)
    if user_data is None:
        database.create_user(update.effective_user, str(update.effective_chat.id))

        await update.message.reply_text(
            f'Welcome {update.effective_user.first_name}! 🤗\n'
            'I am not quite ready yet, but I will be soon.\n\n'
            'Would you like to join the wailist to receive an invitation when I am ready?',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboards['waitlist'], 
                one_time_keyboard=True, 
                input_field_placeholder='Yes/No'
                )
        )
        return WAITLIST
    
    else:
        if user_data['is_enabled'] == 1:
            await update.message.reply_text(
                f'Hi {update.effective_user.first_name}!\n'
                'I am ready to help you finding a car rental. 🚗\n\n'
                'Type "/help" to see a list of available commands.'
            )
            ########################################### TODO: Add preferred city ###########################################
            return ConversationHandler.END
        
        if user_data['has_accepted_communications'] == 0:
            await update.message.reply_text(
                f'Hi {update.effective_user.first_name}!\n'
                'I am still not quite ready yet.\n\n'
                'Would you like to join the wailist now to receive an invitation when I am ready?',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboards['waitlist'], 
                one_time_keyboard=True, 
                input_field_placeholder='Yes/No'
                )
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

    elif update.message.text.lower().startswith('n'):
        await update.message.reply_text('No worries! You can check back here later.',
            reply_markup=ReplyKeyboardRemove()
        )

    else:
        await update.message.reply_text(
            'Sorry, I didn\'t understand that. Please try again.',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboards['waitlist'], 
                one_time_keyboard=True, 
                input_field_placeholder='Yes/No'
                )
        )
        return WAITLIST

    return ConversationHandler.END





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
    'registration': ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WAITLIST: [MessageHandler(filters.Regex(re.compile(r'^(y|n)', re.IGNORECASE)), waitlist)]
        },
        fallbacks=[]
    ),
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