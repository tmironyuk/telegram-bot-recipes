from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove

from loader import dp, db
from data.config import admins
from states import Questions
from keyboards.default import menu_main

from emoji import emojize


@dp.message_handler(text=emojize('Отзыв :pencil2:', use_aliases=True))
async def bot_help(message: types.Message):
    text = '\n'.join([
        'Ты перешёл на страницу отзывов.\nЭто своего рода книга отзывов и предложений. ' +
        'Здесь ты можешь написать всё, что тебе понравилось (или не очень) в работе бота. ' +
        'А я обещаю всё честно передать своему создателю. ' +
        emojize('Твоё мнение очень важно для нас :backhand_index_pointing_right_light_skin_tone:', use_aliases=True) +
        emojize(':backhand_index_pointing_left_light_skin_tone::pleading_face:', use_aliases=True),
        '',
        'Если ты попал сюда случайно, то напиши слово: «Отмена».',
        '',
        'Если ты всё-таки хочешь оставить своё мнение, то можешь написать его ниже:'
    ])
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await Questions.reviews_state.set()


@dp.message_handler(state=Questions.reviews_state)
async def get_review(message: types.Message, state: FSMContext):
    if message.text.lower().strip() == "отмена":
        text = [
            emojize('Эххх...\nСегодня без отзывов :cry:', use_aliases=True),
            '',
            emojize('Чем я ещё могу тебе помочь? :thinking_face:', use_aliases=True)
        ]
        await message.answer(text='\n'.join(text), reply_markup=menu_main)
        await state.reset_state(with_data=False)
    else:
        for admin in admins:
            text_admin = '\n'.join([
                f'Отзыв от: @{message.from_user.username}',
                '',
                f'Имя пользователя: {message.from_user.full_name}',
                '',
                f'#отзывы : {message.text}',
                '',
                f'Дата: {message.date}'
            ])
            await dp.bot.send_message(admin, text_admin)
        db.add_review(id=message.from_user.id,
                      name=message.from_user.full_name,
                      time=message.date,
                      review=message.text,
                      username=f'@{message.from_user.username}')
        text = [
            emojize('Спасибо за твоё мнение, друг! :pray:', use_aliases=True),
            '',
            emojize('Что я ещё могу сделать для тебя? :drooling_face:', use_aliases=True)
        ]
        await message.answer(text='\n'.join(text), reply_markup=menu_main)
        await state.reset_state(with_data=False)
