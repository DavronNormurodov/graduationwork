from users.models import User
from orders.models import Order, OrderProduct
from bot import const
from bot import utils

from geopy.geocoders import Nominatim


def get_user(chat_id):
    user = User.objects.filter(chat_id=chat_id).first()
    if not user:
        return None
    return user


def get_order(user):
    order = Order.objects.filter(user=user, status='active').first()
    if not order:
        return None
    return order


def set_lang(user, lang):
    user.lang = lang
    user.save()


def set_user_info(user, data):
    user.name = data['name']
    user.contact_number = data['contact_number']
    user.save()


def set_name(user, name):
    user.name = name
    user.save()


def set_contact(user, phone_number):
    user.contact_number = phone_number
    user.save()


def set_location(order, location):
    geolocator = Nominatim(user_agent="geoapiExercises")
    Latitude, Longitude = map(str, location)
    order.location = {"latitude": Latitude, "longitude": Longitude}
    order.save()
    location = geolocator.reverse(Latitude + "," + Longitude)
    address = location.raw['address']
    city = address.get('city', '')
    state = address.get('state', '')
    country = address.get('country', '')


def add_to_card(user, product_id, amount):
    order = Order.objects.filter(user=user, status='active').first()
    if order:
        order_product = OrderProduct.objects.filter(order_id=order.id, product_id=product_id).first()
        if not order_product:
            order_product = OrderProduct.objects.create(order_id=order.id, product_id=product_id, amount=int(amount))
        else:
            order_product.amount += int(amount)
            order_product.save()
    else:
        order = Order.objects.create(user=user)
        order_product = OrderProduct.objects.create(order_id=order.id, product_id=product_id, amount=int(amount))
    order.total_price += order_product.product.price * int(amount)
    order.save()


def remove_product_from_card(bot, chat_id, message_id, order, product_id, lang):
    order_product = OrderProduct.objects.get(product_id=product_id)
    order_product.delete()
    order.total_price -= order_product.product.price * order_product.amount
    order.save()
    msg = ''
    if order.products.exists():
        for op in order.products.all():
            msg += f'{op.product.title[lang]}:\n\t\t{op.product.price} \
                * {op.amount} = {op.product.price * op.amount}\n'
        msg += f'{const.TOTAL_PRICE[lang]} = {order.total_price}'
        bot.edit_message_text(msg, chat_id, message_id)
        bot.edit_message_reply_markup(chat_id, message_id,
                                      reply_markup=utils.get_card_info_inline_keyboard(order, lang))
    else:
        order.delete()
        bot.delete_message(chat_id, message_id)
        utils.back_to_main_menu(bot, chat_id, lang)


def clear_the_card(order):
    order.status = 'cancelled'
    order.save()

