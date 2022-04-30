import telebot
from telebot.storage import StateMemoryStorage
# from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters
from telebot.types import (ReplyKeyboardMarkup, KeyboardButton, InputMedia,
                           ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton)
import re

from users.models import User, Admins
from orders.models import Order, OrderProduct
from bot import const, db_utils, utils, senders, askers
from bot.states import UserStates

Token = '5209006621:AAHrVgeVWJWrBUv754umJF-YZ0QnII9RQ9Q'
provider_token = '398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065'
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


@bot.message_handler(state=UserStates.orders.name)
def orders_handler(message):
    user_id, chat_id, msg = utils.get_from_message(message)
    user = db_utils.get_user(chat_id)
    order = db_utils.get_order(user)
    if not user:
        askers.user_not_found(bot, chat_id)
    senders.handle_orders(bot, chat_id, msg, order, user.lang)


@bot.message_handler(content_types=['location'])
def location_handler(message):
    user_id, chat_id, msg = utils.get_from_message(message)
    location = [message.location.latitude, message.location.longitude]
    user = db_utils.get_user(chat_id)
    order = db_utils.get_order(user)
    if not user:
        askers.user_not_found(bot, chat_id)
    db_utils.set_location(order, location)


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
def default_message_handler(message):
    user_id, chat_id, msg = utils.get_from_message(message)
    user = db_utils.get_user(chat_id)
    if not user:
        askers.user_not_found(bot, chat_id)
    bot.send_message(chat_id, const.PRODUCTS[user.lang],
                     reply_markup=utils.get_main_menu_keyboard(user.lang))
    bot.set_state(chat_id, UserStates.main_menu.name)


"""==================================PAYMENT========================================="""

from telebot.types import LabeledPrice, ShippingOption
shipping_options = [
        ShippingOption(id='fast', title='Eng tez').add_price(LabeledPrice('Eng tez', 1000000)),
        ShippingOption(id='one_day', title='Bir kun').add_price(LabeledPrice('Bir kun', 500000)),
        ShippingOption(id='in_person', title='Olib ketish').add_price(LabeledPrice('Olib ketish', -100000))]


@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    user = db_utils.get_user(shipping_query.from_user.id)
    if shipping_query.shipping_address.country_code != 'UZ':
        bot.answer_shipping_query(shipping_query.id, False, shipping_options, const.INVALID_SHIPPING_ADDRESS[user.lang])

    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message=const.TRY_AGAIN[user.lang])


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    user = db_utils.get_user(pre_checkout_query.from_user.id)
    currency = pre_checkout_query.currency
    total_amount = pre_checkout_query.total_amount
    payload = pre_checkout_query.invoice_payload
    shipping_option_id = pre_checkout_query.shipping_option_id
    shipping_address = pre_checkout_query.order_info.shipping_address
    address = f'{shipping_address.city}, {shipping_address.state}, ' \
              f'{shipping_address.street_line1}, {shipping_address.street_line2}'

    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message=const.TRY_AGAIN[user.lang])
    order = db_utils.get_order(user)
    order.shipping_type = shipping_option_id
    order.address = address
    order.total_price = total_amount / 100
    order.status = 'process'
    order.save()
    bot.send_message(pre_checkout_query.from_user.id, const.BACK_MAIN_MENU[user.lang],
                     reply_markup=utils.get_main_menu_keyboard(user.lang))
    bot.set_state(pre_checkout_query.from_user.id, UserStates.main_menu.name)


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    user = db_utils.get_user(message.from_user.id)
    lang = user.lang
    order = Order.objects.get(id=message.successful_payment.invoice_payload)
    bot.send_message(message.chat.id,
                     const.SUCCESS[lang].format(
                         message.successful_payment.total_amount / 100, message.successful_payment.currency),
                     parse_mode='Markdown')
    msg = ""
    for i, op in enumerate(order.products.all()):
        msg += f'{i+1}. {op.product.title[lang]}: {op.amount} x {op.product.price}\n'
    msg += f'\n{const.TOTAL_PRICE[lang]} = {order.total_price}\n'
    msg += f'\n{const.ORDER_USER[lang]}: {user.name}\n'
    msg += f'\n{const.ORDER_PHONE[lang]}: +{user.contact_number}\n'
    msg += f'\n{const.ORDER_ADDRESS[lang]}: {order.address}\n'
    msg += f'\n{const.ORDER_TYPE[lang]}: {order.shipping_type}\n'
    admins = Admins.objects.all()
    for admin in admins:
        bot.send_message(admin.chat_id, msg, reply_markup=utils.inline_keyboard('delivered', f'complete_{order.id}'))


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.from_user.id
    data = call.data
    user = db_utils.get_user(chat_id)
    step = data.split('_')[0]
    _id = data.split('_')[1]
    message_id = call.message.message_id
    if step.split(':')[0] == 'add':
        index, total = step.split(':')[1].split('-')
        askers.show_keyboard_numbers(bot, chat_id, message_id, _id, index, total)
        pass
    elif step in ('forward', 'back'):
        askers.show_next_product(bot, user, _id, message_id, step)
    elif step.split(':')[0] == 'toCard':
        db_utils.add_to_card(user, _id, step.split(':')[1])
    elif step == 'remove':
        order = Order.objects.get(user=user, status='active')
        db_utils.remove_product_from_card(bot, chat_id, message_id, order, _id, user.lang)
    elif step == 'pay':
        order = db_utils.get_order(user)
        prices = []
        for e in order.products.all():
            prices.append(LabeledPrice(e.product.title[user.lang], int(f'{int(e.product.price)}00')))
        msg = const.PAYMENT_NOTIFICATION[user.lang]
        bot.send_invoice(chat_id,
                         title=f'{order.id}',
                         description=msg,
                         provider_token=provider_token,
                         currency='UZS',
                         prices=prices,
                         invoice_payload=f'{order.id}',
                         is_flexible=True)
    elif step == 'complete':
        order = Order.objects.get(id=_id)
        if order.status != 'delivered':
            order.status = 'delivered'
            order.broker = call.from_user.username
            order.save()
            bot.send_message(
                call.message.json.get('chat')['id'],
                const.DELIVERED_BY[user.lang].format(call.from_user.username),
                reply_to_message_id=message_id)
        else:
            bot.send_message(
                call.message.json.get('chat')['id'],
                const.ALREADY_DELIVERED[user.lang].format(call.from_user.username, order.broker),
                reply_to_message_id=message_id
            )


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())

