from aiogram import types
from aiogram.utils.markdown import hbold
from aiogram.dispatcher.storage import FSMContext

from loader import dp, bot
from keyboards.default import menu_main, menu_reset
from states import Questions

from emoji import emojize


@dp.message_handler(text=emojize('Сброс :gun:', use_aliases=True))
async def bot_help(message: types.Message):
    html_text = "\n".join([
        'Ты зашёл на страницу сброса состояний бота.\n\nЕсли в какой-то момент что-то пошло не так, ',
        emojize('ты можешь нажать на кнопку «Сбросить бота :dizzy_face:» и я вернусь в начальное состояние.',
                use_aliases=True),
        '',
        emojize('Если ты попал сюда случайно, нажми кнопку «Отмена :heart_eyes:».', use_aliases=True),
        ''
    ])
    await message.answer(html_text, reply_markup=menu_reset)
    await Questions.reset_state.set()


@dp.message_handler(state=Questions.reset_state)
async def answer_ingredients(message: types.Message, state: FSMContext):
    if message.text == emojize('Сбросить бота :dizzy_face:', use_aliases=True):
        await state.finish()
        html_text = "\n".join([
            'Вот что ты наделал?!\nЯ обнулился...',
            '',
            emojize('Чувствую себя великолепно, будто заново родился! :angel:', use_aliases=True),
            '',
            'Давай попробуем начать сначала. Чем я могу тебе помочь?'
        ])
        await bot.send_photo(chat_id=message.chat.id,
                             photo='https://i0.wp.com/ivi.ru/titr/uploads/2017/04/10/327039a888764f0fe4f438146817dc5f.jpg',
                             caption=html_text,
                             reply_markup=menu_main)
        await state.reset_state(with_data=False)
    elif message.text == emojize('Отмена :heart_eyes:', use_aliases=True):
        html_text = "\n".join([
            emojize('Фуууух... Пронесло! :confetti_ball:', use_aliases=True),
            '',
            emojize('Что делаем дальше? :stuck_out_tongue_winking_eye:', use_aliases=True)
        ])
        await message.answer(html_text, reply_markup=menu_main)
        await state.reset_state(with_data=False)
    else:
        html_text = "\n".join([
            emojize('Кажется, ты промахнулся мимо кнопок на клавиатуре... :sweat_smile:', use_aliases=True),
            '',
            emojize('Что делаем дальше, босс? :zany_face:', use_aliases=True)
        ])
        await message.answer(html_text, reply_markup=menu_main)
        await state.reset_state(with_data=False)
