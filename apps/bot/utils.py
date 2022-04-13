from telebot.types import (ReplyKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)


from bot import db_utils, const
from users.models import User
from products.models import Product, Category


def get_language_keyboard():
    rkm = ReplyKeyboardMarkup(True, row_width=2)
    rkm.add(const.LANG_CHOOSE_MENU['uz'], const.LANG_CHOOSE_MENU['ru'])
    return rkm


def get_main_menu_keyboard(lang):
    rkm = ReplyKeyboardMarkup(True, row_width=2)
    rkm.add(const.PRODUCTS[lang])
    rkm.add(const.CARD[lang], const.ABOUT_US[lang])
    rkm.add(const.SETTINGS[lang])
    return rkm


def get_settings_menu_keyboard(lang):
    rkm = ReplyKeyboardMarkup(True)
    rkm.add(const.LANG_SETTINGS[lang], const.NAME_SETTINGS[lang], const.CONTACT_SETTINGS[lang])
    rkm.add(const.BACK[lang])
    return rkm


def get_categories_keyboard(lang):
    rkm = ReplyKeyboardMarkup(True, row_width=2)
    categories = Category.objects.filter(parent=None)
    c = [category for category in categories]
    count = len(c)
    i = 0
    while i < count:
        if not count % 2:
            rkm.add(c[i].title[lang], c[i+1].title[lang])
            i += 2
        else:
            if i == count - 1:
                rkm.add(c[i].title[lang])
                i += 2
            else:
                rkm.add(c[i].title[lang], c[i + 1].title[lang])
                i += 2
    rkm.add(const.BACK[lang])
    return rkm


def get_subcategories_keyboard(lang, cat):
    rkm = ReplyKeyboardMarkup(True, row_width=2)
    categories = cat.children.all()
    c = [category for category in categories]
    count = len(c)
    i = 0
    while i < count:
        if not count % 2:
            rkm.add(c[i].title[lang], c[i + 1].title[lang])
            i += 2
        else:
            if i == count - 1:
                rkm.add(c[i].title[lang])
                i += 2
            else:
                rkm.add(c[i].title[lang], c[i + 1].title[lang])
                i += 2
    rkm.add(const.BACK[lang])
    return rkm


def get_inline_products(product):
    ikbs = (
        InlineKeyboardButton('◀️', callback_data=f'back_{product.id}'),
        InlineKeyboardButton(f"{product.id}/{5}", callback_data='2'),
        InlineKeyboardButton("▶️", callback_data=f'forward_{product.id}')
    )
    ikb = InlineKeyboardButton('add to card', callback_data=f'add_{product.id}'),
    ikm = InlineKeyboardMarkup()
    ikm.add(*ikbs)
    ikm.add(*ikb)
    return ikm


def get_from_message(message):
    return message.from_user.id, message.chat.id, message.text


def set_category(cat):
    with open('apps/bot/category.txt', 'w') as f:
        f.write(f'{cat.id}')


def get_category():
    with open('apps/bot/category.txt') as f:
        cat_id = f.read()
    if cat_id:
        cat = Category.objects.get(id=cat_id)
        if cat.parent:
            if cat.parent.parent:
                return cat.parent.parent
            else:
                return 1
    return None
