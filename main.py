import asyncio
import pymorphy2
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from config import BOT_TOKEN, QIWI_TOKEN
from db import Database
from pyqiwip2p import QiwiP2P

bot = Bot(BOT_TOKEN, parse_mode='html') # Переменная bot отвечает за авторизацию c с помощью токена
dp = Dispatcher(bot, storage=MemoryStorage()) # Диспетчер отвечает за обработку событий: нажатие кнопок, отправка сообщений и файлов и т.д.
morph = pymorphy2.MorphAnalyzer()
db = Database('db.db')  # Создаём экзепляр класса "Database" и передаём название БД
p2p = QiwiP2P(auth_key=QIWI_TOKEN)

def tfidf_tokenize(text):
  return list(map(lambda word: morph.parse(word)[0].normal_form, text.split()))

class ClientStates(StatesGroup):
  main_state = State()
  start_news_processing = State()
  language_state = State()
  price_list = State()
  buy_subscription = State()

if __name__ == '__main__':
  from handlers import dp, on_startup # Импортируем halndlers тут, так как main импортируется в handlers и, при обычном импорте, возникнет циркулярное импортирование
  executor.start_polling(dp, on_startup=on_startup, skip_updates=True)  # Запуск бот-сервера в режиме поллинга