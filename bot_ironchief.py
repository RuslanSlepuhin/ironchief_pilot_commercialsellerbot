from aiogram import Bot, Dispatcher, executor, types
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import datetime
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

token = '5428081252:AAHZPr6jiAe5pS2tp8k-38QZt0rgEZIoUIk'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

msg_list = []

print(f'Bot started at {datetime.datetime.now()}')
def main():

    @dp.message_handler(commands=['start'])
    async def welcome_user(message):
        await delete_messages(len(msg_list))
        # await bot.send_message(message.chat.id, f'{message.chat.id}\n{message.from_user.username}\n{message.from_user.first_name}\n{message.from_user.last_name}')
        print(f'{message.chat.id}\n{message.from_user.username}\n{message.from_user.first_name}\n{message.from_user.last_name}')

        await bot.delete_message(message.chat.id, message.message_id)
        msg_list.append(await bot.send_message(message.chat.id, f'Привет, <b>{message.from_user.first_name}</b>!\n'
                                                                f'Этот бот поможет выбрать и заказать товар\n\n'
                                                                f'P.S. В нашем инстаграм постим с сторис промо-коды со скидосами до -20%\n'
                                                                f'https://instagram.com/ironchef.by?igshid=YmMyMTA2M2Y=',
                                               parse_mode='html'))
        category_list = {'names':['мусаты зеркальные', 'охотничьи ножи', 'колбаса от Юрченко'], 'callbacks': ['musat', 'hunting', 'jurchenko']}
        markup = await online_menu(category_list, row_width=4)
        msg_list.append(await bot.send_message(message.chat.id, 'Популярные запросы', reply_markup=markup, parse_mode='html'))

    @dp.message_handler(content_types=['text'])
    async def some_text(message):
        await bot.delete_message(message.chat.id, message.message_id)
        await delete_messages(len(msg_list))
        markup = await online_menu({'names': ['назад в меню'], 'callbacks': ['catalog']})
        msg_list.append(await bot.send_message(message.chat.id, 'я еще не сделал ответы на текст, чуть позже, бро', reply_markup=markup))

    @dp.callback_query_handler()
    async def catch_callback(callback: types.CallbackQuery):

        global msg_list

        match callback.data:
            case 'musat':
                await delete_messages(len(msg_list))
                await send_musat_descriptions(callback.message)

            case 'hunting':
                await delete_messages(len(msg_list))
                markup = await online_menu({'names': ['загнутый', 'прямой', 'черный'], 'callbacks': ['circle', 'pr', 'black']})
                msg_list.append(await bot.send_message(callback.message.chat.id, 'Выберите какой нож', reply_markup=markup))

            case 'jurchenko':
                await delete_messages(len(msg_list))
                markup = await online_menu(
                    {'names': ['назад в меню'], 'callbacks': ['catalog']})
                msg_list.append(await bot.send_message(callback.message.chat.id, 'Здесь может быть колбаса от юрченко',
                                                       reply_markup=markup))

            case 'order':
                await delete_messages(len(msg_list))
                markup = await online_menu(
                    {'names': ['назад в меню'], 'callbacks': ['catalog']})
                msg_list.append(await bot.send_message(callback.message.chat.id, 'Ваш заказ отправлен, ожидайте звонка в течение часа', reply_markup=markup))

            case 'call':
                await delete_messages(len(msg_list))
                markup = await online_menu(
                    {'names': ['назад в меню'], 'callbacks': ['catalog']})
                msg_list.append(await bot.send_message(callback.message.chat.id, '+375 29 6449690 Людмила Борисовна', reply_markup=markup))

            case 'circle':
                await delete_messages(len(msg_list))
                await send_hunting_descriptions(callback.message)

            case 'pr':
                await delete_messages(len(msg_list))
                markup = await online_menu(
                    {'names': ['назад в меню'], 'callbacks': ['catalog']})
                msg_list.append(await bot.send_message(callback.message.chat.id, 'Здесь будет картинка с ножом', reply_markup=markup))

            case 'black':
                await delete_messages(len(msg_list))
                markup = await online_menu(
                    {'names': ['назад в меню'], 'callbacks': ['catalog']})
                msg_list.append(await bot.send_message(callback.message.chat.id, 'Здесь будет картинка с ножом', reply_markup=markup))

            case 'catalog':
                await delete_messages(len(msg_list))
                category_list = {'names': ['мусаты зеркальные', 'охотничьи ножи', 'колбаса от Юрченко'],
                                 'callbacks': ['musat', 'hunting', 'jurchenko']}
                markup = await online_menu(category_list, row_width=4)
                msg_list.append(await bot.send_message(callback.message.chat.id, 'Популярные запросы', reply_markup=markup, parse_mode='html'))

            case 'to_basket':
                await delete_messages(len(msg_list))
                button_basket = KeyboardButton('Корзина')
                stand_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_basket)
                message_basket = await bot.send_message(callback.message.chat.id,
                                                        'Вы можете перейти в корзину в любой момент для дальнейшего заказа',
                                                        reply_markup=stand_markup, parse_mode='html')

                markup = await online_menu({'names': ['назад в меню'], 'callbacks': ['catalog']})
                msg_list.append(await bot.send_message(callback.message.chat.id, 'Товар отправлен в корзину',
                                   reply_markup=markup))




            case 'basket':
                await delete_messages(len(msg_list))
                markup = await online_menu(
                    {'names': ['назад в меню'], 'callbacks': ['catalog']})
                msg_list.append(
                    msg_list.append(await bot.send_message(callback.message.chat.id, 'Отобразиться всё, что положил в корзину', reply_markup=markup)))


    executor.start_polling(dp, skip_updates=True)

async def online_menu(category_list, row_width=1):
    n=0
    markup = InlineKeyboardMarkup(row_width=row_width)
    while n<len(category_list['names']):
        markup.add(InlineKeyboardButton(category_list['names'][n], callback_data=category_list['callbacks'][n]))
        n += 1
    return markup


async def send_musat_descriptions(message):
    description = f'<b>49 euro</b>\n\nНасечка: средняя насечка\n' \
                  f'Форма: овал\n' \
                  f'Назначение: Предназначен для восстановления режущей кромки ножей\n' \
                  f'\nрежет всех животных на куски, не оставляя вопросов. Рекомендует Юрченко для охоты\n' \
                  f'для того, чтобы услышать профессиональное мнение, можете к нам в канал обвальщиков http://t.me/obval'
    category_list = {'names': ['Заказать', 'Позвонить', 'В корзину', 'Назад в каталог'], 'callbacks': ['order', 'call', 'to_basket', 'catalog']}
    markup = await online_menu(category_list, row_width=2)
    msg_list.append(await bot.send_photo(message.chat.id, 'http://www.гиссер.бел/assets/cache_image/files/Musat/9905_31_1000x0_600.jpeg', caption=description, reply_markup=markup, parse_mode='html'))

async def send_hunting_descriptions(message):
    description = f'<b>49 euro</b>\n\nНасечка: средняя насечка\n' \
                  f'Материал лезвия: Высококачественная  хромомолибденовая сталь. Твердость по Роквеллу 56 – 57\n' \
                  f'Назначение: Нож обвалочный, очень гибкий\n' \
                  f'Особенности лезвия: Лезвие с прямой заточкой. Очень гибкий\n' \
                  f'\nрежет всех животных на куски, не оставляя вопросов. Рекомендует Юрченко для охоты\n' \
                  f'для того, чтобы услышать профессиональное мнение, можете к нам в канал обвальщиков http://t.me/obval'
    category_list = {'names': ['Заказать', 'Позвонить', 'В корзину', 'Назад в каталог'], 'callbacks': ['order', 'call', 'to_basket', 'catalog']}
    markup = await online_menu(category_list, row_width=2)
    msg_list.append(await bot.send_photo(message.chat.id,
                                         'http://giesser-bel.by/assets/cache_image/files/ab_popular/12253_15_1000x0_1a8.jpg',
                                         caption=description, reply_markup=markup, parse_mode='html'))

async def delete_messages(numbers):

    global msg_list

    for i in range(0, numbers):
        try:
            await msg_list[-1].delete()
            msg_list.pop(-1)
        except:
            msg_list = []
            break

# main()

