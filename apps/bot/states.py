from telebot.handler_backends import State, StatesGroup


# class State:
#     def __init__(self, name=None) -> None:
#         self.name = name
#
#     def __str__(self) -> str:
#         return self.name


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
    subcategories = State()


