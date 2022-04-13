from bot import const, utils, db_utils
from bot.states import UserStates
from users.models import User
from products.models import Product

from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup


def ask_language(bot, chat_id):
    bot.send_message(chat_id, const.ASK_LANGUAGE, reply_markup=utils.get_language_keyboard(), parse_mode='HTML')
    bot.set_state(chat_id, UserStates.language.name)


def ask_name(bot, chat_id, lang):
    bot.send_message(chat_id, const.ASK_NAME[lang], parse_mode='HTML', reply_markup=ReplyKeyboardRemove())
    bot.set_state(chat_id, UserStates.name.name)


def ask_contact(bot, chat_id, lang):
    bot.send_message(chat_id, const.ASK_CONTACT_NUMBER[lang], parse_mode='HTML')
    bot.set_state(chat_id, UserStates.contact.name)


def not_valid_lang(bot, chat_id):
    bot.send_message(chat_id, 'Tilni keyboard orqali tanlang\nВыберите язык с помощью клавиатуры')


def about_us(bot, chat_id, lang):
    bot.send_message(chat_id, const.ABOUT_US_INFO[lang])


def show_settings(bot, chat_id, lang):
    bot.send_message(chat_id, const.SETTING_MESSAGE[lang], reply_markup=utils.get_settings_menu_keyboard(lang))
    bot.set_state(chat_id, UserStates.settings.name)


def show_categories(bot, chat_id, lang):
    bot.send_message(chat_id, const.PRODUCTS[lang].split()[1], reply_markup=utils.get_categories_keyboard(lang))
    bot.set_state(chat_id, UserStates.categories.name)


def show_sub_categories(bot, chat_id, lang, cat):
    bot.send_message(chat_id, const.PRODUCTS[lang].split()[1], reply_markup=utils.get_subcategories_keyboard(lang, cat))
    # bot.set_state(chat_id, UserStates.subcategories.name)


def show_products(bot, chat_id, lang, cat):
    product = Product.objects.filter(category=cat).order_by('id').first()
    if product:
        caption = f'{product.title[lang]}\n\n{product.price}'
        bot.send_photo(chat_id, product.image, caption, reply_markup=utils.get_inline_products(product))
    else:
        bot.send_message(chat_id, const.PRODUCT_DOES_NOT_EXIST[lang])


def show_next_product(bot, user, product_id, message_id, step):
    chat_id = user.chat_id
    product_cat = Product.objects.get(id=product_id).category
    products = Product.objects.filter(category=product_cat).order_by('id')

    next_product = products.filter(id__gt=product_id).first() if step == 'forward' \
        else products.filter(id__lt=product_id).last()
    if next_product:
        caption = f'{next_product.title[user.lang]}\n\n{next_product.price}'
        bot.delete_message(chat_id, message_id)
        bot.send_photo(chat_id, next_product.image, caption,
                       reply_markup=utils.get_inline_products(next_product))
    else:
        next_product = products.first() if step == 'forward' else products.last()
        caption = f'{next_product.title[user.lang]}\n\n{next_product.price}'
        bot.delete_message(chat_id, message_id)
        bot.send_photo(chat_id, next_product.image, caption,
                       reply_markup=utils.get_inline_products(next_product))


def ask_lang_change(bot, chat_id, lang):
    rkm = utils.get_language_keyboard()
    rkm.add(const.BACK[lang])
    bot.send_message(chat_id, const.ASK_LANGUAGE, reply_markup=rkm)
    bot.set_state(chat_id, UserStates.lang_change.name)


def ask_name_change(bot, chat_id, lang):
    rkm = ReplyKeyboardMarkup(True).add(const.BACK[lang])
    bot.send_message(chat_id, const.ASK_NAME[lang], reply_markup=rkm)
    bot.set_state(chat_id, UserStates.name_change.name)


def ask_contact_change(bot, chat_id, lang):
    rkm = ReplyKeyboardMarkup(True).add(const.BACK[lang])
    bot.send_message(chat_id, const.ASK_CONTACT_NUMBER[lang], reply_markup=rkm)
    bot.set_state(chat_id, UserStates.contact_change.name)


def user_not_found(bot, chat_id):
    bot.send_message(chat_id, f"{const.USER_NOT_FOUND['uz']}\n{const.USER_NOT_FOUND['ru']}")


def user_requisites(bot, chat_id):
    user = db_utils.get_user(chat_id)
    if not user:
        User.objects.create(chat_id=chat_id)
        ask_language(bot, chat_id)
    elif not user.lang:
        ask_language(bot, chat_id)
    elif not user.name:
        ask_name(bot, chat_id, user.lang)
    elif not user.contact_number:
        ask_contact(bot, chat_id, user.lang)
    else:
        bot.send_message(chat_id, const.EXIST_USER_STARTED[user.lang],
                         reply_markup=utils.get_main_menu_keyboard(user.lang))
        bot.set_state(chat_id, UserStates.main_menu.name)
