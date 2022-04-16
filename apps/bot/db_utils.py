from users.models import User
from orders.models import Order, OrderProduct
from bot import const


def get_user(chat_id):
    user = User.objects.filter(chat_id=chat_id).first()
    if not user:
        return None
    return user


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
    order.total_price += order_product.product.price
    order.save()
