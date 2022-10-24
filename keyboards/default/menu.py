from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from emoji import emojize


menu_main = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=emojize('Справка :eyes:', use_aliases=True))
                ],
                [
                    KeyboardButton(text=emojize('Категории :fork_and_knife:', use_aliases=True)),
                    KeyboardButton(text=emojize('Ингредиенты :shrimp:', use_aliases=True))
                ],
                [
                    KeyboardButton(text=emojize('Рецепты :book:', use_aliases=True))
                ],
                [
                    KeyboardButton(text=emojize('Отзыв :pencil2:', use_aliases=True)),
                    KeyboardButton(text=emojize('Сброс :gun:', use_aliases=True))
                ],
            ],
            resize_keyboard=True
        )

menu_recipes = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=emojize('Предыдущая страница :arrow_left:', use_aliases=True)),
            KeyboardButton(text=emojize('Следующая страница :arrow_right:', use_aliases=True))
        ],
        [
            KeyboardButton(text=emojize('Справка :eyes:', use_aliases=True))
        ],
        [
            KeyboardButton(text=emojize('Категории :fork_and_knife:', use_aliases=True)),
            KeyboardButton(text=emojize('Ингредиенты :shrimp:', use_aliases=True))
        ],
        [
            KeyboardButton(text=emojize('Рецепты :book:', use_aliases=True))
        ],
        [
            KeyboardButton(text=emojize('Отзыв :pencil2:', use_aliases=True)),
            KeyboardButton(text=emojize('Сброс :gun:', use_aliases=True))
        ],
    ],
    resize_keyboard=True
)

menu_reset = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=emojize('Сбросить бота :dizzy_face:', use_aliases=True)),
            KeyboardButton(text=emojize('Отмена :heart_eyes:', use_aliases=True))
        ],
    ],
    resize_keyboard=True
)
