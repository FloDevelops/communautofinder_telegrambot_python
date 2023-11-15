from reservauto import client
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
from telegrambot_reservauto.utilities.orm import Database

reservauto_client = client.ReservautoClient()
branches = reservauto_client.branches
cities = []

database = Database()

SET_CITY, SAVE_CITY = range(2)

async def ask_branch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Sets the preferred branch'''

    if branches is None:
        await update.message.reply_text(
            'Sorry, I couldn\'t get the list of branches. Please try again later.'
        )
        return ConversationHandler.END
    
    await update.message.reply_text(
        'Please choose your preferred branch:',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[branch['branchLocalizedName']] for branch in branches], 
            one_time_keyboard=True, 
            input_field_placeholder='Branch'
            )
    )
    return SET_CITY


async def ask_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Sets the preferred city'''

    if update.message.text not in [branch['branchLocalizedName'] for branch in branches]:
        await update.message.reply_text(
            'Sorry, I didn\'t understand. Please try again.'
        )
        return SET_CITY
    
    branch_id = [branch['branchId'] for branch in branches if branch['branchLocalizedName'] == update.message.text][0]
    print(branch_id)
    cities.extend(reservauto_client.get_cities(branch_id=branch_id))
    print(cities)

    await update.message.reply_text(
        'Please choose your preferred city:',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[city['cityLocalizedName']] for city in cities],
            one_time_keyboard=True,
            input_field_placeholder='City'
            )
    )
    return SAVE_CITY


async def save_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''Saves the preferred city'''

    if update.message.text not in [city['cityLocalizedName'] for city in cities]:
        await update.message.reply_text(
            'Sorry, I didn\'t understand. Please try again.'
        )
        return SAVE_CITY
    
    city_id = [city['cityId'] for city in cities if city['cityLocalizedName'] == update.message.text][0]
    updates = {'preferred_city_id': city_id}
    database.update_user(telegram_user=update.effective_user, updates=updates)

    await update.message.reply_text(
        'Your preferred city has been saved.'
    )
    return ConversationHandler.END


def account_conv_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('account', ask_branch)],
        states={
            SET_CITY: [MessageHandler(filters.TEXT, ask_city)],
            SAVE_CITY: [MessageHandler(filters.TEXT, save_city)]
        },
        fallbacks=[]
    )