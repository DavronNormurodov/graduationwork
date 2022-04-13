from bot.states import UserStates
from bot import const, db_utils, utils, askers
from products.models import Category, Product
import re


def get_lang(bot, chat_id, msg, user):
    if msg == const.LANG_CHOOSE_MENU['uz']:
        db_utils.set_lang(user, 'uz')
        askers.ask_name(bot, chat_id, user.lang)
    elif msg == const.LANG_CHOOSE_MENU['ru']:
        db_utils.set_lang(user, 'ru')
        askers.ask_name(bot, chat_id, user.lang)
    else:
        askers.not_valid_lang(bot, chat_id)


def get_name(bot, chat_id, msg, lang):
    if msg.isalpha():
        with bot.retrieve_data(chat_id) as data:
            data['name'] = msg
        askers.ask_contact(bot, chat_id, lang)
    else:
        bot.send_message(chat_id, const.INVALID_NAME_MESSAGE[lang])


def get_contact(bot, chat_id, msg, user):
    if re.match(r'^998[0-9]{9}$', msg):
        with bot.retrieve_data(chat_id) as data:
            data['contact_number'] = msg
            db_utils.set_user_info(user, data)
        bot.send_message(chat_id, const.ACCESS_MESSAGE[user.lang],
                         reply_markup=utils.get_main_menu_keyboard(user.lang))
        bot.set_state(chat_id, UserStates.main_menu.name)
    else:
        bot.send_message(chat_id, const.INVALID_CONTACT_MESSAGE[user.lang])


def handle_main_menu(bot, chat_id, msg, lang):
    if msg == const.ABOUT_US[lang]:
        askers.about_us(bot, chat_id, lang)
    if msg == const.SETTINGS[lang]:
        askers.show_settings(bot, chat_id, lang)
    if msg == const.PRODUCTS[lang]:
        askers.show_categories(bot, chat_id, lang)


def handle_categories(bot, chat_id, msg, lang):
    if msg == const.BACK[lang]:
        cat = utils.get_category()
        if not cat:
            bot.send_message(chat_id, const.BACK_MAIN_MENU[lang], reply_markup=utils.get_main_menu_keyboard(lang))
            bot.set_state(chat_id, UserStates.main_menu.name)
        elif cat == 1:
            askers.show_categories(bot, chat_id, lang)
            utils.set_category(Category.objects.filter(parent=None).first())
        else:
            askers.show_sub_categories(bot, chat_id, lang, cat)
            if cat.children.all():
                utils.set_category(cat.children.first())
            else:
                utils.set_category(cat)
    else:
        cat = None
        for c in Category.objects.all():
            if c.title[lang] == msg:
                cat = c
                break
        if cat:
            if cat.children.all():
                utils.set_category(cat.children.first())
            else:
                utils.set_category(cat)
            if not cat.children.all():
                askers.show_products(bot, chat_id, lang, cat)
            else:
                askers.show_sub_categories(bot, chat_id, lang, cat)


def handle_settings_menu(bot, chat_id, msg, lang):
    if msg == const.BACK[lang]:
        bot.send_message(chat_id, const.BACK_MAIN_MENU[lang], reply_markup=utils.get_main_menu_keyboard(lang))
        bot.set_state(chat_id, UserStates.main_menu.name)
    elif msg == const.LANG_SETTINGS[lang]:
        askers.ask_lang_change(bot, chat_id, lang)
    elif msg == const.NAME_SETTINGS[lang]:
        askers.ask_name_change(bot, chat_id, lang)
    elif msg == const.CONTACT_SETTINGS[lang]:
        askers.ask_contact_change(bot, chat_id, lang)


def handle_lang_change(bot, chat_id, msg, user):
    lang = user.lang
    if msg == const.BACK[lang]:
        bot.send_message(chat_id, const.BACK[lang].split()[0], reply_markup=utils.get_settings_menu_keyboard(lang))
        bot.set_state(chat_id, UserStates.settings.name)
    elif msg == const.LANG_CHOOSE_MENU['uz']:
        db_utils.set_lang(user, 'uz')
        bot.send_message(chat_id, "✅", reply_markup=utils.get_settings_menu_keyboard('uz'))
        bot.set_state(chat_id, UserStates.settings.name)
    elif msg == const.LANG_CHOOSE_MENU['ru']:
        db_utils.set_lang(user, 'ru')
        bot.send_message(chat_id, "✅", reply_markup=utils.get_settings_menu_keyboard('ru'))
        bot.set_state(chat_id, UserStates.settings.name)
    else:
        askers.not_valid_lang(bot, chat_id)


def handle_name_change(bot, chat_id, msg, user):
    lang = user.lang
    if msg == const.BACK[lang]:
        bot.send_message(chat_id, const.BACK[lang].split()[0], reply_markup=utils.get_settings_menu_keyboard(lang))
        bot.set_state(chat_id, UserStates.settings.name)
    elif msg.isalpha():
        db_utils.set_name(user, msg)
        bot.send_message(chat_id, "✅", reply_markup=utils.get_settings_menu_keyboard(lang))
        bot.set_state(chat_id, UserStates.settings.name)
    else:
        bot.send_message(chat_id, const.INVALID_NAME_MESSAGE[user.lang])


def handle_contact_change(bot, chat_id, msg, user):
    lang = user.lang
    if msg == const.BACK[lang]:
        bot.send_message(chat_id, const.BACK[lang].split()[0], reply_markup=utils.get_settings_menu_keyboard(lang))
        bot.set_state(chat_id, UserStates.settings.name)
    elif re.match(r'^998[0-9]{9}$', msg):
        db_utils.set_contact(user, msg)
        bot.send_message(chat_id, "✅", reply_markup=utils.get_settings_menu_keyboard(lang))
        bot.set_state(chat_id, UserStates.settings.name)
    else:
        bot.send_message(chat_id, const.INVALID_CONTACT_MESSAGE[lang])
