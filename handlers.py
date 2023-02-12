from aiogram.types import Message, CallbackQuery, Update
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from main import bot, dp, db, ClientStates
from keyboards import get_start_reply_keyboard, get_finish_reply_keyboard, get_lang_inline_keyboard, remove_reply_keyboard
from use_model import predict_news
from translations import _

async def on_startup(_) -> None:  # Метод, который предназначен для исполнения во время запуска бот-сервера
  print('Бот-сервер запущен')


@dp.message_handler(commands=['start']) # Декоратор асинхронной функции для обработки команды "/start" 
async def start_command(message: Message) -> None:
  if not db.user_exists(message.from_user.id):  # Проверка на наличие пользователя в БД
    db.add_user(message.from_user.id, message.from_user.first_name, 'ru') # Добавление пользователя в БД
  lang = db.get_lang(message.from_user.id)  # Получение языка пользователя
  hi_message = f'<b>{_("Здравствуйте",lang)}</b>,\
  <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>.\n'
  Tg_ID = f'{_("Ваш Telegram ID", lang)}: <code>{message.from_user.id}</code>'
  await ClientStates.main_state.set() # Установка состояния конечного автомата
  await message.answer(text=(hi_message+Tg_ID)) # Отвечаем на сообщение "/start" от пользователя
  await bot.send_sticker(message.from_user.id, sticker=f'{_("CAACAgIAAxkBAAEHqsRj5gntHgyhS50H9BvijKtAeEjh1wACuwIAAjrRBwABoYHYWwuDTsEuBA",lang)}', reply_markup=get_start_reply_keyboard(lang))  # Отправляем приветственный стикер
  await message.delete() # Удаляем сообщение "/start" от пользователя, чтобы не было спама

@dp.message_handler(state=ClientStates.main_state)
async def start_button_pressed(message: Message) -> None:
  lang = db.get_lang(message.from_user.id)  # Получение языка пользователя
  if (message.text == _('Начать работу', lang)):
    await ClientStates.start_news_processing.set() # Установка состояния конечного автомата
    await message.answer(text=_('Отправь мне текст новости', lang), reply_markup=get_finish_reply_keyboard(lang))
    await message.delete()
  elif (message.text == _('Сменить язык', lang)):
    await ClientStates.language_state.set() # Установка состояния конечного автомата
    await message.answer(text=_('Выбери язык', lang), reply_markup=get_lang_inline_keyboard())
    await message.delete()
  elif (message.text == '/start'):
    hi_message = f'<b>{_("Здравствуйте",lang)}</b>,\
    <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>.\n'
    Tg_ID = f'{_("Ваш Telegram ID", lang)}: <code>{message.from_user.id}</code>'
    await ClientStates.main_state.set() # Установка состояния конечного автомата
    await message.answer(text=(hi_message+Tg_ID)) # Отвечаем на сообщение "/start" от пользователя
    await bot.send_sticker(message.from_user.id, sticker=f'{_("CAACAgIAAxkBAAEHqsRj5gntHgyhS50H9BvijKtAeEjh1wACuwIAAjrRBwABoYHYWwuDTsEuBA",lang)}', reply_markup=get_start_reply_keyboard(lang))  # Отправляем приветственный стикер
    await message.delete() # Удаляем сообщение "/start" от пользователя, чтобы не было спама
  else :
    await message.answer(text=_('Некорректный ввод', lang))
    await message.delete()

@dp.message_handler(lambda message: message.text, content_types=['text'], state=ClientStates.start_news_processing)
async def load_news(message: Message, state: FSMContext) -> None:
  lang = db.get_lang(message.from_user.id)  # Получение языка пользователя
  if (message.text==_('Сменить язык', lang)):
    await ClientStates.language_state.set() # Установка состояния конечного автомата
    await message.answer(text=_('Выбери язык', lang), reply_markup=get_lang_inline_keyboard())
    await message.delete()
  elif (message.text==_('Завершить работу', lang)):
    await message.answer(text=_('Работа завершена', lang), reply_markup=get_start_reply_keyboard(lang))
    await ClientStates.main_state.set() # Установка состояния конечного автомата
    await message.delete()
  elif (message.text == '/start'):
    hi_message = f'<b>{_("Здравствуйте",lang)}</b>,\
    <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>.\n'
    Tg_ID = f'{_("Ваш Telegram ID", lang)}: <code>{message.from_user.id}</code>'
    await ClientStates.main_state.set() # Установка состояния конечного автомата
    await message.answer(text=(hi_message+Tg_ID)) # Отвечаем на сообщение "/start" от пользователя
    await bot.send_sticker(message.from_user.id, sticker=f'{_("CAACAgIAAxkBAAEHqsRj5gntHgyhS50H9BvijKtAeEjh1wACuwIAAjrRBwABoYHYWwuDTsEuBA",lang)}', reply_markup=get_start_reply_keyboard(lang))  # Отправляем приветственный стикер
    await message.delete() # Удаляем сообщение "/start" от пользователя, чтобы не было спама
  else:
    predict = await predict_news(message.text)  # Передача текста классификатору
    if predict>=0.6:
      await message.answer(text=f'✅ {_("Новость является истинной с вероятностью", lang)} {predict*100}%')
    elif predict<=0.45:
      await message.answer(text=f'❌ {_("Новость является фейком с вероятностью", lang)} {predict*100}%')
    else:
      await message.answer(text=f'⁉️ {_("Затрудняюсь определить, заслуживает ли полученная информация доверия", lang)}')

@dp.message_handler(content_types=['any'], state=ClientStates.start_news_processing)
async def check_news(message: Message) -> None:
  lang = db.get_lang(message.from_user.id)  # Получение языка пользователя
  await message.reply(_('Это не текст новости!', lang))

@dp.message_handler(state=ClientStates.language_state)
async def any_input(message: Message) -> None:
  lang = db.get_lang(message.from_user.id)  # Получение языка пользователя
  if (message.text == '/start'):
    hi_message = f'<b>{_("Здравствуйте",lang)}</b>,\
    <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>.\n'
    Tg_ID = f'{_("Ваш Telegram ID", lang)}: <code>{message.from_user.id}</code>'
    await ClientStates.main_state.set() # Установка состояния конечного автомата
    await message.answer(text=(hi_message+Tg_ID)) # Отвечаем на сообщение "/start" от пользователя
    await bot.send_sticker(message.from_user.id, sticker=f'{_("CAACAgIAAxkBAAEHqsRj5gntHgyhS50H9BvijKtAeEjh1wACuwIAAjrRBwABoYHYWwuDTsEuBA",lang)}', reply_markup=get_start_reply_keyboard(lang))  # Отправляем приветственный стикер
    await message.delete() # Удаляем сообщение "/start" от пользователя, чтобы не было спама
  else:
    await message.answer(text=_('Некорректное действие', lang))
    await message.delete()


@dp.callback_query_handler(text_contains='lang_', state=ClientStates.language_state) # Обработчик события нажатия на кнопку смены языка
async def set_lang(callback: CallbackQuery, state: FSMContext) -> None:
  await  callback.message.delete()  # Удаляем сообщение с кнопками выбора языка
  await ClientStates.main_state.set() # Установка состояния конечного автомата
  lang = callback.data[5:]
  db.change_lang(callback.from_user.id, lang)
  hi_message = f'<b>{_("Здравствуйте",lang)}</b>,\
  <a href="tg://user?id={callback.from_user.id}">{callback.from_user.first_name}</a>.\n'
  Tg_ID = f'{_("Ваш Telegram ID", lang)}: <code>{callback.from_user.id}</code>'
  await bot.send_message(callback.from_user.id, text=(hi_message+Tg_ID)) # Отвечаем на сообщение "/start" от пользователя
  await bot.send_sticker(callback.from_user.id, sticker=f'{_("CAACAgIAAxkBAAEHqsRj5gntHgyhS50H9BvijKtAeEjh1wACuwIAAjrRBwABoYHYWwuDTsEuBA",lang)}', reply_markup=get_start_reply_keyboard(lang))  # Отправляем приветственный стикер
  return














@dp.message_handler(commands=['sticker'])
async def sticker(message: Message):
  await bot.send_sticker(message, sticker = "CAACAgIAAxkBAAEHqsRj5gntHgyhS50H9BvijKtAeEjh1wACuwIAAjrRBwABoYHYWwuDTsEuBA", reply_markup=ikb1)

@dp.callback_query_handler(text='start_work')
async def cb_start_work(callback: CallbackQuery):
  await  callback.message.delete_reply_markup()
  await bot.send_message(callback.message.chat.id, text='Введите новость', reply_markup=ikb1)  # Отправляем приветственный стикер
  return

@dp.callback_query_handler(lambda callback_query: callback_query.data=='')
async def cb_start_work(callback: CallbackQuery):
  await  bot.edit_message_text('Новое меню, кнопка 1', callback.message.chat.id, callback.message.message_id, reply_markup=ikb1)


@dp.errors_handler(exception=BotBlocked) # Обработка исключения, если пользователь заблокировал бота
async def error_bot_blocked_handler(update: Update, exception: BotBlocked):
  print('Бот остановлен или заблокирован!')
  return True