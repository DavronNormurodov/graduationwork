from telebot.types import (ReplyKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)


from bot import db_utils, const
from users.models import User
from products.models import Product, Category
from .states import UserStates


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
    products = Product.objects.filter(category=product.category).order_by('id')
    index = [p for p in products].index(product)
    total = products.count()
    ikbs = (
        InlineKeyboardButton('??????', callback_data=f'back_{product.id}'),
        InlineKeyboardButton(f"{index+1}/{total}", callback_data=f'www_{product.id}'),
        InlineKeyboardButton("??????", callback_data=f'forward_{product.id}')
    )
    ikb = InlineKeyboardButton('???', callback_data=f'add:{index+1}-{total}_{product.id}'),
    ikm = InlineKeyboardMarkup()
    ikm.add(*ikbs)
    ikm.add(*ikb)
    return ikm


def get_inline_keyboard_numbers(product_id, index, total):
    ikbs = [
        InlineKeyboardButton('??????', callback_data=f'back_{product_id}'),
        InlineKeyboardButton(f"{index}/{total}", callback_data=f'tt_{product_id}'),
        InlineKeyboardButton("??????", callback_data=f'forward_{product_id}')
    ]
    for i in range(1, 10):
        ikbs.append(InlineKeyboardButton(f'{i}', callback_data=f'toCard:{i}_{product_id}'))
    ikm = InlineKeyboardMarkup()
    ikm.add(*ikbs)
    return ikm


def get_card_info_keyboard(order, lang):
    rkm = ReplyKeyboardMarkup(True, row_width=2)
    kb = KeyboardButton(const.LOCATION[lang], request_location=True)
    rkm.add(const.CLEAR_CARD[lang], const.ORDER[lang])
    # rkm.add(kb, const.ORDER_DESCRIPTION[lang])
    rkm.add(kb,)
    rkm.add(const.BACK[lang])
    return rkm


def get_card_info_inline_keyboard(order, lang):
    ikm = InlineKeyboardMarkup()
    order_products = order.products.all()
    ikm.add(*[InlineKeyboardButton(f'{op.product.title[lang]}???', callback_data=f'remove_{op.product.id}') for op in order_products])
    return ikm


def get_payment_inline_keyboard(order, lang):
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton(const.PAYMENT[lang], callback_data=f'pay_{order.id}'))
    return ikm


def get_from_message(message):
    return message.from_user.id, message.chat.id, message.text


def back_to_main_menu(bot, chat_id, lang):
    bot.send_message(chat_id, const.BACK_MAIN_MENU[lang], reply_markup=get_main_menu_keyboard(lang))
    bot.set_state(chat_id, UserStates.main_menu.name)


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


def inline_keyboard(text, data):
    ikm = InlineKeyboardMarkup()
    ikm.add(InlineKeyboardButton(text, callback_data=data))
    return ikm
