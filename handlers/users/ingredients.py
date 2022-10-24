from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove

from loader import dp
from states import Questions
from data import dataset_search
from keyboards.default import menu_main

from emoji import emojize
import nltk
import re


@dp.message_handler(text=emojize('Ингредиенты :shrimp:', use_aliases=True))
async def get_ingredients(message: types.Message):
    text = '\n'.join([
        'Ну что ж, давайте выберем ингредиенты!',
        '',
        'Перечисли через запятую все продукты, из которых ты хочешь что-нибудь приготовить.'
    ])
    await message.answer(text=text,
                         reply_markup=ReplyKeyboardRemove())
    await Questions.ingredients_state.set()


@dp.message_handler(state=Questions.ingredients_state)
async def answer_ingredients(message: types.Message, state: FSMContext):
    def request_to_list(request):
        def clear_txt(txt):
            txt = txt.lower()
            txt = re.sub('[^a-zA-Zа-яА-ЯёЁ]', ' ', txt)
            new_txt = ''
            for word in txt.split(' '):
                if len(word) > 0:
                    new_txt += word + ' '
            return new_txt[:-1]

        my_list = []
        text = request.split(',')
        for word in text:
            word_iter = clear_txt(word)
            if word_iter:
                my_list.append(word_iter)
        return my_list

    def get_recipes_nltk(text):
        if text:
            min_distance = 1
            near_category = ''
            words = text.split(' ')
            for word in words:
                if word in dataset_search:
                    word_dataset = dataset_search[word]
                    for ingredient, category in word_dataset:
                        distance = nltk.edit_distance(text, ingredient) / len(ingredient)
                        if distance < min_distance:
                            min_distance = distance
                            near_category = category
            if min_distance != 1 and len(text) > 2:
                return near_category
            else:
                return 'НЕТ'
        return 'НЕТ'

    answer = message.text
    list_request = request_to_list(answer)
    list_ingredient = []
    if len(list_request) == 0:
        text = '\n'.join([
            emojize('Друг, ты не ввёл ни одного ингредиента :woozy_face:', use_aliases=True),
            '',
            emojize('Попробуй ввести хотя бы несколько, для этого нажми на кнопку «Ингредиенты :shrimp:»',
                    use_aliases=True)
        ])
        await message.answer(text=text,
                             reply_markup=menu_main)
        await state.reset_state(with_data=False)
    else:
        for term in list_request:
            ingredient = get_recipes_nltk(term)
            if ingredient != 'НЕТ':
                list_ingredient.append(ingredient)
                continue
            list_ingredient.append(ingredient)
        count_fail = 0
        clear_ingredient = []
        fail_ingredient = []
        for i in range(len(list_ingredient)):
            if list_ingredient[i] == 'НЕТ':
                count_fail += 1
                fail_ingredient.append(list_request[i])
            else:
                clear_ingredient.append(list_ingredient[i])
        if fail_ingredient:
            text = ''.join([
                'К своему несчастью, я не смог разобрать следующие ',
                emojize('ингредиенты: {} :cry:'.format(', '.join(fail_ingredient)), use_aliases=True)
            ])
            await message.answer(text=text)

        if len(clear_ingredient) > 10:
            text = '\n'.join([
                emojize('Ты ввёл слишком много ингредиентов :exploding_head:', use_aliases=True),
                '',
                emojize('Пока что я могу подобрать рецепты не более чем для 10 ингредиентов :see_no_evil:',
                        use_aliases=True),
                '',
                'Уменьши количество продуктов и попробуй ещё раз, ' +
                emojize('для этого нажми на кнопку «Ингредиенты :shrimp:»', use_aliases=True)
            ])
            await message.answer(text=text,
                                 reply_markup=menu_main)
            await state.reset_state(with_data=False)

        elif count_fail == len(list_ingredient):
            text = '\n'.join([
                emojize('Мне очень стыдно, но я не смог разобрать ни один твой ингредиент :sob:', use_aliases=True),
                '',
                emojize('Попробуй ввести заново, для этого нажми на кнопку «Ингредиенты :shrimp:»', use_aliases=True)
            ])
            await message.answer(text=text,
                                 reply_markup=menu_main)
            await state.reset_state(with_data=False)

        elif count_fail != 0:
            async with state.proxy() as data:
                data['ingredients'] = clear_ingredient
            data = await state.get_data()
            if data.get('category'):
                text = '\n'.join([
                    'Но ничего страшного! ' +
                    emojize('Я всё равно что-нибудь подберу из оставшихся ингредиентов! :face_with_rolling_eyes:',
                            use_aliases=True),
                    '',
                    emojize('Категории твоих ингредиентов: {} :ok_hand:'.format(', '.join(clear_ingredient)),
                            use_aliases=True),
                    '',
                    'Если я ошибся, попробуй уточнить или переформулировать ингредиент, ' +
                    emojize('для этого нажми на кнопку «Ингредиенты :shrimp:» ещё раз.', use_aliases=True),
                    '',
                    emojize('Если всё ок, то переходи к рецептам, нажимая на «Рецепты :book:».', use_aliases=True)
                ])
                await message.answer(text=text,
                                     reply_markup=menu_main)
                await state.reset_state(with_data=False)
            else:
                text = '\n'.join([
                    'Но ничего страшного! ' +
                    emojize('Я всё равно что-нибудь подберу из оставшихся ингредиентов! :face_with_rolling_eyes:',
                            use_aliases=True),
                    '',
                    emojize('Категории твоих ингредиентов: {} :ok_hand:'.format(', '.join(clear_ingredient)),
                            use_aliases=True),
                    '',
                    'Если я ошибся, попробуй уточнить или переформулировать ингредиент, ' +
                    emojize('для этого нажми на кнопку «Ингредиенты :shrimp:» ещё раз.', use_aliases=True),
                    '',
                    'Если всё супер, то выбирай ' +
                    emojize('«Категории :fork_and_knife:» блюд.', use_aliases=True)
                ])
                await message.answer(text=text,
                                     reply_markup=menu_main)
                await state.reset_state(with_data=False)
        else:
            async with state.proxy() as data:
                data['ingredients'] = clear_ingredient
            data = await state.get_data()
            if data.get('category'):
                text = '\n'.join([
                    emojize('Категории твоих ингредиентов: {} :ok_hand:'.format(', '.join(clear_ingredient)),
                            use_aliases=True),
                    '',
                    'Если я ошибся, попробуй уточнить или переформулировать ингредиент, ' +
                    emojize('для этого нажми на кнопку «Ингредиенты :shrimp:» ещё раз.', use_aliases=True),
                    '',
                    emojize('Если всё супер, то жми скорей на «Рецепты :book:».\n\nА то они уже стынут!', use_aliases=True)
                ])
                await message.answer(text=text,
                                     reply_markup=menu_main)
                await state.reset_state(with_data=False)
            else:
                text = '\n'.join([
                    emojize('Категории твоих ингредиентов: {} :ok_hand:'.format(', '.join(clear_ingredient)),
                            use_aliases=True),
                    '',
                    'Если я ошибся, попробуй уточнить или переформулировать ингредиент, ' +
                    emojize('для этого нажми на кнопку «Ингредиенты :shrimp:» ещё раз.', use_aliases=True),
                    '',
                    'Если всё супер, то выбирай ' +
                    emojize('«Категории :fork_and_knife:» блюд.', use_aliases=True)
                ])
                await message.answer(text=text,
                                     reply_markup=menu_main)
                await state.reset_state(with_data=False)
