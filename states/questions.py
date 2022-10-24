from aiogram.dispatcher.filters.state import StatesGroup, State


class Questions(StatesGroup):
    ingredients_state = State()
    category_state = State()
    recipe_state = State()
    current_page = State()
    reviews_state = State()
    reset_state = State()
