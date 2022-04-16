import telebot
from telebot.storage import StateMemoryStorage
# from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters
from telebot.types import (ReplyKeyboardMarkup, KeyboardButton, InputMedia,
                           ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)
import re

from users.models import User
from bot import const, db_utils, utils, senders, askers
from bot.states import UserStates

Token = '5209006621:AAHrVgeVWJWrBUv754umJF-YZ0QnII9RQ9Q'
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(token=Token, state_storage=state_storage)


@bot.message_handler(commands=['del'])
def command_help(message):
    chat_id = message.from_user.id
    User.objects.get(chat_id=chat_id).delete()
    bot.send_message(chat_id, 'Deleted', reply_markup=ReplyKeyboardRemove())


@bot.message_handler(commands=['start'])
def command_help(message):
    chat_id = message.from_user.id
    askers.user_requisites(bot, chat_id)


@bot.message_handler(state=UserStates.language.name)
def language_set_handler(message):
    user_id, chat_id, msg = utils.get_from_message(message)
    user = db_utils.get_user(chat_id)
    if not user:
        askers.user_not_found(bot, chat_id)
    senders.get_lang(bot, chat_id, msg, user)


@bot.message_handler(state=UserStates.name.name)
def name_set_handler(message):
    user_id, chat_id, msg = utils.get_from_message(message)
    user = db_utils.get_user(chat_id)
    if not user:
        askers.user_not_found(bot, chat_id)
    senders.get_name(bot, chat_id, msg, user.lang)


@bot.message_handler(state=UserStates.contact.name)
def contact_set_handler(message):
    user_id, chat_id, msg = utils.get_from_message(message)
    user = db_utils.get_user(chat_id)
    if not user:
        askers.user_not_found(bot, chat_id)
    senders.get_contact(bot, chat_id, msg, user)


@bot.message_handler(state=UserStates.main_menu.name)
def main_menu_handler(message):
    user_id, chat_id, msg = utils.get_from_message(message)
    user = db_utils.get_user(chat_id)
    if not user:
        askers.user_not_found(bot, chat_id)
    senders.handle_main_menu(bot, chat_id, msg, user.lang)


@bot.message_handler(state=UserStates.categories.name)
def categories_handler(message):
    user_id, chat_id, msg = utils.get_from_message(message)
    user = db_utils.get_user(chat_id)
    if not user:
        askers.user_not_found(bot, chat_id)
    senders.handle_categories(bot, chat_id, msg, user.lang)


@bot.message_handler(state=UserStates.settings.name)
def settings_handler(message):
    user_id, chat_id, msg = utils.get_from_message(message)
    user = db_utils.get_user(chat_id)
    if not user:
        askers.user_not_found(bot, chat_id)
    senders.handle_settings_menu(bot, chat_id, msg, user.lang)


@bot.message_handler(state=UserStates.lang_change.name)
def lang_change_handler(message):
    user_id, chat_id, msg = utils.get_from_message(message)
    user = db_utils.get_user(chat_id)
    if not user:
        askers.user_not_found(bot, chat_id)
    senders.handle_lang_change(bot, chat_id, msg, user)


@bot.message_handler(state=UserStates.name_change.name)
def name_change_handler(message):
    user_id, chat_id, msg = utils.get_from_message(message)
    user = db_utils.get_user(chat_id)
    if not user:
        askers.user_not_found(bot, chat_id)
    senders.handle_name_change(bot, chat_id, msg, user)


@bot.message_handler(state=UserStates.contact_change.name)
def main_menu_handler(message):
    user_id, chat_id, msg = utils.get_from_message(message)
    user = db_utils.get_user(chat_id)
    if not user:
        askers.user_not_found(bot, chat_id)
    senders.handle_contact_change(bot, chat_id, msg, user)


@bot.message_handler(func=lambda msg: True)
def main_menu_handler(message):
    user_id, chat_id, msg = utils.get_from_message(message)
    user = db_utils.get_user(chat_id)
    if not user:
        askers.user_not_found(bot, chat_id)
    bot.send_message(chat_id, const.PRODUCTS[user.lang],
                     reply_markup=utils.get_main_menu_keyboard(user.lang))
    bot.set_state(chat_id, UserStates.main_menu.name)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.from_user.id
    data = call.data
    user = db_utils.get_user(chat_id)
    step = data.split('_')[0]
    product_id = data.split('_')[1]
    message_id = call.message.message_id
    if step == 'add':
        askers.show_keyboard_numbers(bot, chat_id, message_id, product_id, user.lang)
        pass
    elif step in ('forward', 'back'):
        askers.show_next_product(bot, user, product_id, message_id, step)
    elif step.split(':')[0] == 'toCard':
        db_utils.add_to_card(user, product_id, step.split(':')[1])


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

