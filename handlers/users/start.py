from aiogram import types
from aiogram.utils.markdown import hbold, hitalic, hunderline, hlink, code

from loader import dp, bot, db
from data.config import admins
from keyboards.default import menu_main

from emoji import emojize


@dp.message_handler(text=['/start'])
async def bot_start(message: types.Message):
    html_text = "\n".join([
        emojize(f'Привет, {message.from_user.first_name}! :wave:', use_aliases=True),
        '',
        'Меня зовут бот Накормил))))))).',
        'Я подберу тебе меню из тех продуктов, что есть у тебя в холодильнике.',
        '',
        emojize('Чтобы узнать, как со мной работать, нажми на кнопку «Справка :eyes:».', use_aliases=True)
    ])
    await bot.send_photo(chat_id=message.chat.id,
                         photo='https://static.wikia.nocookie.net/rutube9658/images/e/eb/%D0%9F%D0%BE%D0%B2%D0%B0%D1%80.jpg/revision/latest/scale-to-width-down/340?cb=20170205091925&path-prefix=ru',
                         caption=html_text,
                         reply_markup=menu_main)
    db.add_user(id=message.from_user.id,
                name=message.from_user.full_name,
                time=message.date,
                username=f'@{message.from_user.username}')
    for admin in admins:
        text_admin = '\n'.join([
            f'Бот запущен: @{message.from_user.username}',
            '',
            f'Имя пользователя: {message.from_user.full_name}',
            '',
            f'#старт : {message.date}'
        ])
        await dp.bot.send_message(admin, text_admin)
