from aiogram import types
from aiogram.types import ContentType
from aiogram.dispatcher.storage import FSMContext
from aiogram.utils.markdown import hitalic

from loader import dp
from keyboards.default import menu_main, menu_recipes

from emoji import emojize


@dp.message_handler(content_types=ContentType.ANY)
async def bot_echo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.get('recipes'):
        html_text = "\n".join(
            [
                'Дружище!',
                'Ты пишешь что-то не то...',
                '',
                emojize('Воспользуйся справкой! :alien:', use_aliases=True),
                '',
                hitalic('Если у тебя пропало меню навигации, то разверни его') +
                emojize(hitalic('\nвооооооооооооооот тут :arrow_lower_right:'), use_aliases=True)]
        )
        await message.answer(text=html_text,
                             reply_markup=menu_recipes)
    else:
        html_text = "\n".join(
            [
                'Дружище!',
                'Ты пишешь что-то не то...',
                '',
                emojize('Воспользуйся справкой! :alien:', use_aliases=True),
                '',
                hitalic('Если у тебя пропало меню навигации, то разверни его') +
                emojize(hitalic('\nвооооооооооооооот тут :arrow_lower_right:'), use_aliases=True)]
        )
        await message.answer(text=html_text,
                             reply_markup=menu_main)
