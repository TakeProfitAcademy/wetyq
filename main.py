
from os import stat
from aiogram import Bot, Dispatcher, executor
from aiogram import types
from contextlib import suppress
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from asyncio import sleep
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging



TOKEN = '5422086034:AAFINdqI4TZyR19sMcdxwNMNeU7v4qbrlNg'

# ? Настройка логирования в stdout
logging.basicConfig(
    level=logging.INFO,
    format=u"%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

# ? Подключение логгера
logger = logging.getLogger(__name__)


bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# * Определяем стейты для FSM
class MainStates(StatesGroup):
    antichaos = State()
    crypto = State()


button_1 = types.KeyboardButton('Курсы')
button_2 = types.KeyboardButton('О команде')
button_3 = types.KeyboardButton('Услуги')
button_4 = types.KeyboardButton('Поддержка 🛠')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.add(button_1, button_2, button_3, button_4)


ku = types.ReplyKeyboardMarkup(resize_keyboard=True)
b_1 = types.KeyboardButton('Three whales')
b_2 = types.KeyboardButton('Supernal')
ku.add(b_1, b_2)


course_kbd = types.ReplyKeyboardMarkup(resize_keyboard=True)
bt1 = types.KeyboardButton('Программа курса')
bt2 = types.KeyboardButton('Тарифы')
bt3 = types.KeyboardButton('Поддержка 🛠')
bt4 = types.KeyboardButton('Назад ↩️')
course_kbd.add(bt1, bt2, bt3, bt4)


pk1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
bk1 = types.KeyboardButton('Тарифы')
bk2 = types.KeyboardButton('Поддержка 🛠')
bk3 = types.KeyboardButton('Назад ↩️')
pk1.add(bk1, bk2, bk3)


op = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Оплата картой 💳')
item2 = types.KeyboardButton('Оплата через кошелёк(крипта)📈')
back = types.KeyboardButton('Назад ↩️')
op.add(item1, item2, back)

# state="*" означает, что этот хэндлер будет работать при любом стэйте
@dp.message_handler(commands="start", state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish() # Завершение активного стейта
    await message.answer("Привет! Это Take Profit Academy!", reply_markup=greet_kb)


@dp.message_handler(text="Курсы", state="*")
async def courses(message: types.Message):
    with open('st.png', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
    await message.answer("Пожалуйста, выберете курс!", reply_markup=ku)


@dp.message_handler(text="Поддержка 🛠", state="*")
async def support(message: types.Message):
    await message.answer("Оставьте свой вопрос и в ближайшее время с вами свяжется менеджер!\n https://t.me/ManagerTPA", reply_markup=greet_kb)


@dp.message_handler(text='Three whales', state="*")
async def antishaos(message: types.Message, state: FSMContext):
    await MainStates.antichaos.set() # устанавливаем стейт. теперь будут работать только те хэндлеры, в которых есть state=MainStates.antichaos
    with open('ant.png', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
    await message.answer("Информация о курсе!", reply_markup=course_kbd)


@dp.message_handler(text='Supernal', state="*")
async def crypto_x(message: types.Message):
    await MainStates.crypto.set()
    with open('crp.png', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
    await message.answer("Информация о курсе!", reply_markup=course_kbd)


# Программа курса антихаос
# state=MainStates.antichaos = этот хендлер будет работать только в этом стейте
@dp.message_handler(text="Программа курса", state=MainStates.antichaos)
async def course_prog_antichaos(message: types.Message, state: FSMContext):
    with open('pk.png', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
    await message.answer("Программа курса!", reply_markup=course_kbd)



# Тарифы антихаос
@dp.message_handler(text="Тарифы", state=MainStates.antichaos)
async def tarifs_antichaos(message: types.Message, state: FSMContext):
    with open('crpop.png', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
    await message.answer("Выберете способ оплаты!", reply_markup=op)
    

# Программа криптофигни
@dp.message_handler(text="Программа курса", state=MainStates.crypto)
async def course_prog_crypto(message: types.Message, state: FSMContext):
     with open('pkc.png', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
        await message.answer("Программа курса!", reply_markup=course_kbd)



# Тарифы криптофигни
@dp.message_handler(text="Тарифы", state=MainStates.crypto)
async def tarifs_crypto(message: types.Message, state: FSMContext):
    with open('antop.png', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
    await message.answer("Выберете способ оплаты!", reply_markup=op)


@dp.message_handler(text='Оплата картой 💳', state="*")
async def payment_card(message: types.Message):
    await message.answer(
        "Номер карты(Tinkoff): 5536 9141 2107 0563 \n\nПосле оплаты ОБЯЗАТЕЛЬНО отправьте чек в чат https://t.me/ManagerTPA"
        "\n\nВнимательно проверьте скопированный номер карты!\n\n"
        "С уважением - TPA", reply_markup=greet_kb)


@dp.message_handler(text='Оплата через кошелёк(крипта)📈', state="*")
async def payment_wallet(message: types.Message):
    with open('555.png', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
    await message.answer("BTC (Bitcoin): 1Ltpb6whSuuCnY715SVGJr9bkNL8Z8ssCa\n\nUSDT (TRC20): TEzUbW6FJNQvT2DmxsM6sjysWDCbG6wjEp\n\nUSDT (ERC20): 0x0da931073e03e65ef7ee628e53b19df95e052cd8\n\nПосле оплаты ОБЯЗАТЕЛЬНО отправьте Txid транзакции (либо цифры если внутренний перевод Binance) менеджеру:https://t.me/ManagerTPA\n\nВнимательно проверьте скопированный номер кошелька!\n\nС уважением - TPA", reply_markup=greet_kb)



@dp.message_handler(text="О команде", state="*")
async def about_us(message: types.Message):
    with open('kkk.png', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
    await message.answer("Главная информация о нашей команде!", reply_markup=greet_kb)



@dp.message_handler(text="Назад ↩️", state="*")
async def go_back(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Главное меню", reply_markup=greet_kb)



@dp.message_handler(text="Вопросы и ответы❔", state="*")
async def faq(message: types.Message):
    with open('nn.png', 'rb') as file:
        await bot.send_photo(message.chat.id, file)
    await message.answer("Часто задаваемые вопросы!", reply_markup=greet_kb)


@dp.message_handler(text="Услуги", state="*")
async def services(message: types.Message):
    await message.answer("В данном канале предоставлены все услуги от TPA: https://t.me/servstpa", reply_markup=greet_kb)


if __name__ == "__main__":

    # * Запуск поллинга
    try:
        logger.warning("Starting bot")
        executor.start_polling(dp)
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
