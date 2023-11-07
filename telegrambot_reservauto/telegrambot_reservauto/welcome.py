import re
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    filters,
    MessageHandler,
)
from telegrambot_reservauto.orm import Database

database = Database()

WAITLIST = range(0)

keyboards = {
    'waitlist': [['Yes, keep me updated ✅', 'No, I\'ll chech back myself ❌']]
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

def start_conv_handler(): 
    return ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WAITLIST: [MessageHandler(filters.Regex(re.compile(r'^(y|n)', re.IGNORECASE)), waitlist)]
        },
        fallbacks=[]
    )