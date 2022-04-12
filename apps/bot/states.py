from telebot.handler_backends import State, StatesGroup


class UserStates(StatesGroup):
    token = State()
    new_start = State()
    language = State()
    name = State()
    contact = State()
    main_menu = State()
    settings = State()
    lang_change = State()
    name_change = State()
    contact_change = State()
    categories = State()
    products = State()

