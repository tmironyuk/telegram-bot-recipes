from aiogram import types
from aiogram.utils.markdown import hbold

from loader import dp
from keyboards.default import menu_main

from emoji import emojize


@dp.message_handler(text=emojize('Справка :eyes:', use_aliases=True))
async def bot_help(message: types.Message):
    html_text = "\n".join([
            hbold('Кнопки:'),
            emojize('«Справка :eyes:» — получить справку;', use_aliases=True),
            emojize('«Категории :fork_and_knife:» — выбрать категории рецептов;', use_aliases=True),
            emojize('«Ингредиенты :shrimp:» — выбрать продукты;', use_aliases=True),
            emojize('«Рецепты :book:» — получить рецепты;', use_aliases=True),
            emojize('«Отзыв :pencil2:» — книга отзывов и предложений;', use_aliases=True),
            emojize('«Сброс :gun:» — сбросить бота и начать сначала.', use_aliases=True),
            '',
            hbold('Команды:'),
            '/start — Начать диалог.'
    ])
    await message.answer(html_text, reply_markup=menu_main)
