import re
from datetime import datetime
from reservauto import client
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, Location
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
from telegrambot_reservauto.utilities.logger import CustomLogger
from telegrambot_reservauto.utilities.orm import Database

logger = CustomLogger(__name__)
logger.set_level(20)
reservauto_client = client.ReservautoClient()
database = Database()
SEARCH_TYPE, SEARCH_STATION, SEARCH_STATION_RETURN, SEARCH_STATION_LOCATION, SEARCH_STATION_RADIUS, SEARCH_STATION_RESULTS, SEARCH_FLEX = range(7)
keyboards = {
    'search_type': [['Station', 'Flex']]
}


def location_to_dict(location: Location, radius_km: float):
    # Convert the radius from kilometers to degrees (1 degree = 111.32 kilometers)
    radius_degrees = radius_km / 111.32

    # Return the result as a dictionary
    return {
        'min_latitude': location.latitude - radius_degrees,
        'max_latitude': location.latitude + radius_degrees,
        'min_longitude': location.longitude - radius_degrees,
        'max_longitude': location.longitude + radius_degrees,
    }




async def start_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Searches for a car rental'''

    logger.info('Starting search...')

    # Check if the user is already in the database
    user_data = database.get_user(update.effective_user.id)
    if user_data is None or user_data['is_enabled'] == 0:
        logger.info('User is not in the database or is not enabled. Sending message...')
        await update.message.reply_text(
            'Sorry I am not quite available yet.'
        )
        logger.info('Conversation ended.')
        return ConversationHandler.END
    
    logger.info('User is in the database and is enabled. Asking for search type...')
    await update.message.reply_text(
        'Are you looking for a car in station or a Flex car?',
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboards['search_type'], 
                one_time_keyboard=True, 
                input_field_placeholder='Station/Flex'
                )
    )
    logger.info('Moving to search type state.')
    return SEARCH_TYPE



async def check_type_ask_departure_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Routes the user to the correct search function'''

    logger.info('Checking search type...')

    if update.message.text.lower().startswith('s'):
        logger.info('User is looking for a car in station. Asking for departure date and time...')
        await update.message.reply_text(
            'When is your departure date and time? (YYYY-MM-DD HH:MM)',
            reply_markup=ReplyKeyboardRemove()
        )
        return SEARCH_STATION_RETURN    
    
    elif update.message.text.lower().startswith('f'):
        logger.info('User is looking for a Flex car. Asking for location...')
        await update.message.reply_text(
            # 'Please send me your location so I can find the closest Flex car.'
            'This feature is not yet available.',
            reply_markup=ReplyKeyboardRemove()
        )
        return SEARCH_FLEX
    
    else:
        logger.info('User did not enter a valid search type. Asking again...')
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

    logger.info('Checking departure date and time...')

    if re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$', update.message.text) is None:
        logger.info('User did not enter a valid departure date and time. Asking again...')
        await update.message.reply_text(
            'Sorry, I didn\'t understand that. Please try again.',
        )
        return SEARCH_STATION_RETURN

    logger.info('User entered a valid departure date and time. Asking for return date and time...')
    context.user_data['departure'] = update.message.text
    await update.message.reply_text(
        'When is your return date and time? (YYYY-MM-DD HH:MM)'
    )
    return SEARCH_STATION_LOCATION



async def check_return_ask_location_search_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Asks the user for the location'''

    logger.info('Checking return date and time...')

    if re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$', update.message.text) is None:
        logger.info('User did not enter a valid return date and time. Asking again...')
        await update.message.reply_text(
            'Sorry, I didn\'t understand that. Please try again.',
        )
        return SEARCH_STATION_LOCATION
    
    logger.info('User entered a valid return date and time. Asking for location...')
    context.user_data['return'] = update.message.text
    await update.message.reply_text(
        'Please share the location of the area you want to search in (in location attachment)'
    )
    return SEARCH_STATION_RADIUS



async def check_location_ask_radius_search_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Asks the user for the radius'''

    logger.info('Checking location...')

    if update.message.location is None:
        logger.info('User did not send a location. Asking again...')
        await update.message.reply_text(
            'Sorry, I didn\'t understand that. Please try again.',
        )
        return SEARCH_STATION_RADIUS
    
    logger.info(update.message.location)
    logger.info('User sent a location. Asking for radius...')
    context.user_data['location'] = update.message.location
    await update.message.reply_text(
        'Please enter the radius of your search area in km (e.g. 0.5, 1, 2)'
    )
    return SEARCH_STATION_RESULTS



async def check_radius_get_results_search_station(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Shows the results'''

    logger.info('Checking radius...')

    if re.match(r'^\d{1,2}(\.\d{1,2})?$', update.message.text) is None:
        logger.info('User did not enter a valid radius. Asking again...')
        await update.message.reply_text(
            'Sorry, I didn\'t understand that. Please try again.',
        )
        return SEARCH_STATION_RESULTS

    logger.info('User entered a valid radius. Getting results...')
    area = location_to_dict(context.user_data.get('location'), float(update.message.text))
    stations = reservauto_client.get_stations_availability(
        city_id=database.get_user(update.effective_user.id)['preferred_city_id'], 
        min_latitude=area['min_latitude'],
        max_latitude=area['max_latitude'],
        min_longitude=area['min_longitude'],
        max_longitude=area['max_longitude'],
        start_datetime=datetime.strptime(context.user_data.get('departure'), '%Y-%m-%d %H:%M'),
        end_datetime=datetime.strptime(context.user_data.get('return'), '%Y-%m-%d %H:%M')
    )
    stations_string = '\n- '.join([station['stationName'] for station in stations])
    await update.message.reply_text(
        f'Here are the results:\n- {stations_string}'
    )
    logger.info('Conversation ended.')
    return ConversationHandler.END







def search_station_conv_handler(): 
    return ConversationHandler(
        entry_points=[CommandHandler('search', start_search)],
        states={
            SEARCH_TYPE: [MessageHandler(filters.Regex(re.compile(r'^(s|f)', re.IGNORECASE)), check_type_ask_departure_search)],
            SEARCH_STATION_RETURN: [MessageHandler(filters.Regex(re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$')), check_departure_ask_return_search_station)],
            SEARCH_STATION_LOCATION: [MessageHandler(filters.Regex(re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$')), check_return_ask_location_search_station)],
            SEARCH_STATION_RADIUS: [MessageHandler(filters.LOCATION, check_location_ask_radius_search_station)],
            SEARCH_STATION_RESULTS: [MessageHandler(filters.Regex(re.compile(r'^\d{1,2}(\.\d{1,2})?$')), check_radius_get_results_search_station)]
        },
        fallbacks=[]
    )