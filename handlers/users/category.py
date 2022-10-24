from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.markdown import hitalic, hunderline

from loader import dp
from states import Questions
from keyboards.default import menu_main

from emoji import emojize


@dp.message_handler(text=emojize('Категории :fork_and_knife:', use_aliases=True))
async def get_ingredients(message: types.Message):
    html_text = "\n".join(
        [
            'Давай выберем категории!',
            '',
            'Перечисли через запятую категории, которые тебя интересуют.',
            '',
            hunderline('Названия категорий:'),
            '',
            hitalic('Основные блюда, супы, салаты, напитки')]
    )
    await message.answer(text=html_text,
                         reply_markup=ReplyKeyboardRemove())
    await Questions.category_state.set()


@dp.message_handler(state=Questions.category_state)
async def answer_ingredients(message: types.Message, state: FSMContext):
    answer = message.text.lower().split(',')
    list_category = []
    for category in answer:
        i = category.strip()
        if i == 'основные блюда':
            list_category.append('main_recipes')
        elif i == 'супы':
            list_category.append('soups_recipes')
        elif i == 'салаты':
            list_category.append('salades_recipes')
        elif i == 'напитки':
            list_category.append('drinks_recipes')
        else:
            list_category.append('fail')
    if 'fail' in list_category:
        text = '\n'.join([
            'Кажется, у тебя где-то опечатки',
            '',
            emojize('Ещё раз нажми на кнопку «Категории :fork_and_knife:» и попробуй ввести снова.', use_aliases=True)
        ])
        await message.answer(text=text,
                             reply_markup=menu_main)
        await state.reset_state(with_data=False)
    else:
        async with state.proxy() as data:
            data['category'] = list_category
        data = await state.get_data()
        if data.get('ingredients'):
            text = '\n'.join([
                'Категории выбраны, ингредиенты выбраны!',
                '',
                emojize('Скорее нажимай на кнопку «Рецепты :book:»!\n\nОни тебя уже заждались...', use_aliases=True)
            ])
            await message.answer(text=text,
                                 reply_markup=menu_main)
            await state.reset_state(with_data=False)
        else:
            text = '\n'.join([
                'Блеск! Ты определился с категориями!',
                '',
                emojize('Теперь тебе нужно выбрать продукты.\nНажимай на кнопку «Ингредиенты :shrimp:».', use_aliases=True)
            ])
            await message.answer(text=text,
                                 reply_markup=menu_main)
            await state.reset_state(with_data=False)
