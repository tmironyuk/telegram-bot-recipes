import logging

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import category_callback
from loader import dp
from states import Questions

result = dict()

main_recipes_button = 0
if main_recipes_button:
    flag_main = ' ✅'
else:
    flag_main = ''

soups_recipes_button = 0
if main_recipes_button:
    flag_soups = ' ✅'
else:
    flag_soups = ''

salades_recipes_button = 0
if main_recipes_button:
    flag_salades = ' ✅'
else:
    flag_salades = ''

drinks_recipes_button = 0
if main_recipes_button:
    flag_drinks = ' ✅'
else:
    flag_drinks = ''


@dp.message_handler(Command("category"))
async def get_category(message: types.Message):
    choice = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[[InlineKeyboardButton(text='Основные' + flag_main, callback_data='category:1:0:0:0'),
                                                    InlineKeyboardButton(text='Супы' + flag_soups, callback_data='category:0:1:0:0')],
                                                   [InlineKeyboardButton(text='Салаты' + flag_salades, callback_data='category:0:0:1:0'),
                                                    InlineKeyboardButton(text='Напитки' + flag_drinks, callback_data='category:0:0:0:1')],
                                                   [InlineKeyboardButton(text='Готово', callback_data='cancel')]])
    print('первая клавиатура')
    await message.answer(text='Давайте выберем категории', reply_markup=choice)






@dp.callback_query_handler(category_callback.filter(main='1', soups='0', salades='0', drinks='0'))
async def choice_main(call: CallbackQuery, callback_data: dict):
    await call.answer()
    global main_recipes_button
    global result
    if main_recipes_button:
        main_recipes_button = 0
    else:
        main_recipes_button = 1
    print('main_recipes_button =', main_recipes_button)
    logging.info(f"callback_data dict = {callback_data}")
    global flag_main
    if main_recipes_button:
        flag_main = ' ✅'
        print('вторая клавиатура')
        choice = InlineKeyboardMarkup(row_width=2,
                                      inline_keyboard=[[InlineKeyboardButton(text='Основные' + flag_main,
                                                                             callback_data='category:1:0:0:0'),
                                                        InlineKeyboardButton(text='Супы' + flag_soups,
                                                                             callback_data='category:0:0:0:0')],
                                                       [InlineKeyboardButton(text='Салаты' + flag_salades,
                                                                             callback_data='category:0:0:0:0'),
                                                        InlineKeyboardButton(text='Напитки' + flag_drinks,
                                                                             callback_data='category:0:0:0:0')],
                                                       [InlineKeyboardButton(text='Готово', callback_data='cancel')]])
        #result = callback_data
        #print('result', result)
        print('callback_data', callback_data)
        await call.message.answer(f'Вы нажали категорию main, значение переменной {callback_data}', reply_markup=choice)
    else:
        flag_main = ''
        print('третья клавиатура')
        choice1 = InlineKeyboardMarkup(row_width=2,
                                      inline_keyboard=[[InlineKeyboardButton(text='Основные' + flag_main,
                                                                             callback_data='category:0:0:0:0'),
                                                        InlineKeyboardButton(text='Супы' + flag_soups,
                                                                             callback_data='category:0:0:0:0')],
                                                       [InlineKeyboardButton(text='Салаты' + flag_salades,
                                                                             callback_data='category:0:0:0:0'),
                                                        InlineKeyboardButton(text='Напитки' + flag_drinks,
                                                                             callback_data='category:0:0:0:0')],
                                                       [InlineKeyboardButton(text='Готово', callback_data='cancel')]])
        #result = callback_data
        #print('result', result)
        #callback_data = category_callback.new(main='0', soups='0', salades='0', drinks='0')
        print('callback_data', callback_data)
        callback_data = {'@': 'category', 'main': '0', 'soups': '0', 'salades': '0', 'drinks': '0'}
        print('callback_data', callback_data)
        await call.message.answer(f'Вы нажали категорию main, значение переменной {callback_data}', reply_markup=choice1)



@dp.message_handler(category_callback.filter(main='0', soups='0', salades='0', drinks='0'))
async def get_category(message: types.Message):
    choice = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[[InlineKeyboardButton(text='Основные' + flag_main, callback_data='category:1:0:0:0'),
                                                    InlineKeyboardButton(text='Супы' + flag_soups, callback_data='category:0:1:0:0')],
                                                   [InlineKeyboardButton(text='Салаты' + flag_salades, callback_data='category:0:0:1:0'),
                                                    InlineKeyboardButton(text='Напитки' + flag_drinks, callback_data='category:0:0:0:1')],
                                                   [InlineKeyboardButton(text='Готово', callback_data='cancel')]])
    print('поледняя клавиатура')
    await message.answer(text='Давайте выберем категории', reply_markup=choice)

#-----------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------


@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: CallbackQuery):
    global result
    print(result)
    await call.answer("Вы выбрали категории!", show_alert=True)
    await call.message.edit_reply_markup(reply_markup=None)


    # await Questions.category_state.set()


@dp.message_handler(state=Questions.category_state)
async def answer_category(message: types.Message, state: FSMContext):
    answer = message.text
    async with state.proxy() as data:
        data['category'] = answer

    await state.reset_state(with_data=False)
    await message.answer(text='Категории выбраны. Теперь выберите ингредиенты, введя команду /ingredients!')


