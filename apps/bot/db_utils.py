from users.models import User
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
