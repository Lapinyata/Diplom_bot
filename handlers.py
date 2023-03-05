from aiogram.types import Message, CallbackQuery, Update
from aiogram.utils.exceptions import BotBlocked
from aiogram.dispatcher import FSMContext
from main import bot, dp, db, p2p, ClientStates
from keyboards import get_start_reply_keyboard, get_finish_reply_keyboard, get_lang_inline_keyboard, get_subscription_reply_keyboard, get_p2p_inline_keyboard
from use_model import predict_news
from translations import _
import asyncio
import datetime
from dateutil.relativedelta import relativedelta

HELP_COMMAND = """
Данная система предназначена для отбора медицинских новостей и выдачи оценки истинности или ложности полученной информации со степенью уверенности.\n
1) Для того, чтобы начать отбор медицинских новостей, нажмите кнопку "Начать работу".\n
2) Для того, чтобы завершить отбор медицинских новостей, нажмите кнопку "Завершить работу".\n
3) Для того, чтобы изменить язык интерфейса, нажмите кнопку "Сменить язык". В полученном сообщении выберите нужный языковой пакет.\n
4) Для покупки подписки на программную систему нажмите кнопку "Купить подписку".Подписка предоставляет возможность обработки новостных текстов с длиной более 1500 символов.
"""

async def on_startup(_) -> None:  # Метод, который предназначен для исполнения во время запуска бот-сервера
  print('Бот-сервер запущен')

@dp.message_handler(commands=['start', 'restart']) # Декоратор асинхронной функции для обработки команды "/start" 
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

@dp.message_handler(commands=['help'], state=ClientStates.main_state) # Декоратор асинхронной функции для обработки команды "/start" 
async def help_command(message: Message) -> None:
  await message.answer(HELP_COMMAND)
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
  elif (message.text == _('Купить подписку', lang)):
    await ClientStates.price_list.set() # Установка состояния конечного автомата
    cur_date = datetime.datetime.now()
    if (bool(len(db.get_subscription_info(message.from_user.id, cur_date)))):
      await bot.send_message(message.from_user.id, text=f'<b>{_("Текущий статус подписки", lang)}</b>:\n{_("Активна до", lang)} {datetime.datetime.strptime(db.get_subscription_info(message.from_user.id, cur_date)[0][0], "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")}')
      await message.answer(text=_('Возврат в <b>главное меню</b>', lang), reply_markup=get_start_reply_keyboard(lang))
      await ClientStates.main_state.set() # Установка состояния конечного автомата
    else:
      prices = db.get_price_list()
      buy_message = f'{_("Выбран раздел: <b>Купить подписку</b>", lang)}\n'
      current_subscription_state = f'<b>{_("Текущий статус подписки", lang)}</b>:\n<b>{_("Неактивна", lang)}</b>\n'
      price_list_message = f'\n{_("Пожалуйста, ознакомьтесь с прейскурантом", lang)}:\n'
      for position in prices:
        price_list_message = price_list_message + f'• {_(position[1], lang)} = {position[2]}{_("₽", lang)}\n'
      await message.answer(text=(buy_message+current_subscription_state+price_list_message), reply_markup=get_subscription_reply_keyboard(lang))
    await message.delete()
  elif (message.text == '/start' or message.text == '/restart'):
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
  elif (message.text == _('Купить подписку', lang)):
    await ClientStates.price_list.set() # Установка состояния конечного автомата
    cur_date = datetime.datetime.now()
    if (bool(len(db.get_subscription_info(message.from_user.id, cur_date)))):
      await bot.send_message(message.from_user.id, text=f'<b>{_("Текущий статус подписки", lang)}</b>:\n{_("Активна до", lang)} {datetime.datetime.strptime(db.get_subscription_info(message.from_user.id, cur_date)[0][0], "%Y-%m-%d %H:%M:%S.%f").strftime("%Y-%m-%d %H:%M:%S")}')
      await message.answer(text=_('Возврат в <b>главное меню</b>', lang), reply_markup=get_start_reply_keyboard(lang))
      await ClientStates.main_state.set() # Установка состояния конечного автомата
    else:
      prices = db.get_price_list()
      buy_message = f'{_("Выбран раздел: <b>Купить подписку</b>", lang)}\n'
      current_subscription_state = f'<b>{_("Текущий статус подписки", lang)}</b>:\n<b>{_("Неактивна", lang)}</b>\n'
      price_list_message = f'\n{_("Пожалуйста, ознакомьтесь с прейскурантом", lang)}:\n'
      for position in prices:
        price_list_message = price_list_message + f'• {_(position[1], lang)} = {position[2]}{_("₽", lang)}\n'
      await message.answer(text=(buy_message+current_subscription_state+price_list_message), reply_markup=get_subscription_reply_keyboard(lang))
    await message.delete()
  elif (message.text==_('Завершить работу', lang)):
    await message.answer(text=_('Работа завершена', lang), reply_markup=get_start_reply_keyboard(lang))
    await ClientStates.main_state.set() # Установка состояния конечного автомата
    await message.delete()
  elif (message.text == '/help'):
    await ClientStates.main_state.set()
    await message.answer(HELP_COMMAND)
    await message.delete()
  elif (message.text == '/start' or message.text == '/restart'):
    hi_message = f'<b>{_("Здравствуйте",lang)}</b>,\
    <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>.\n'
    Tg_ID = f'{_("Ваш Telegram ID", lang)}: <code>{message.from_user.id}</code>'
    await ClientStates.main_state.set() # Установка состояния конечного автомата
    await message.answer(text=(hi_message+Tg_ID)) # Отвечаем на сообщение "/start" от пользователя
    await bot.send_sticker(message.from_user.id, sticker=f'{_("CAACAgIAAxkBAAEHqsRj5gntHgyhS50H9BvijKtAeEjh1wACuwIAAjrRBwABoYHYWwuDTsEuBA",lang)}', reply_markup=get_start_reply_keyboard(lang))  # Отправляем приветственный стикер
    await message.delete() # Удаляем сообщение "/start" от пользователя, чтобы не было спама
  else:
    cur_date = datetime.datetime.now()
    if (bool(len(db.get_subscription_info(message.from_user.id, cur_date))) or len(message.text)<=1500):
      predict = await predict_news(message.text)  # Передача текста классификатору
      if not db.news_prediction_exists(message.from_user.id, message.text, predict):
        db.download_prediction_result(message.from_user.id, message.text, predict)
      if predict>=0.6:
        await message.answer(text=f'✅ {_("Степень истинности новости равна", lang)} {(predict):.2f}')
      elif predict<=0.45:
        await message.answer(text=f'❌ {_("Степень истинности новости равна", lang)} {(predict):.2f}')
      else:
        await message.answer(text=f'⁉️ {_("Затрудняюсь определить, заслуживает ли полученная информация доверия", lang)}\n{_("Степень истинности новости равна", lang)} {(predict):.2f}')
    elif (len(message.text)>1500):
      await message.answer(text=f'⚡{_("Полученная новость содержит более 1500 символов!", lang)}\n\n{_("<b>Купите подписку</b>, чтобы обрабатывать новости любого размера.", lang)}')

@dp.message_handler(content_types=['any'], state=ClientStates.start_news_processing)
async def check_news(message: Message) -> None:
  lang = db.get_lang(message.from_user.id)  # Получение языка пользователя
  await message.reply(_('Это не текст новости!', lang))

@dp.message_handler(state=ClientStates.language_state)
async def any_input_while_lang_state(message: Message) -> None:
  lang = db.get_lang(message.from_user.id)  # Получение языка пользователя
  if (message.text == '/start' or message.text == '/restart'):
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

array_for_delete_messages=[]

async def buying(message: Message, bill_id) -> None:
  lang = db.get_lang(message.chat.id)  # Получение языка пользователя
  buy_message_id = message
  money_sticker = await bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAEHvdRj66RwIp1bZelkGYm_s2mux95j3QACGQADLdJqJ0kgtejt1lQ5LgQ')
  array_for_delete_messages.append(buy_message_id)
  array_for_delete_messages.append(money_sticker)
  number_of_tryings_to_make_transaction = 280
  while (number_of_tryings_to_make_transaction!=0 and (not str(p2p.check(bill_id=bill_id).status)== "PAID")):
    number_of_tryings_to_make_transaction -= 1
    await asyncio.sleep(3)
  if (str(p2p.check(bill_id=bill_id).status)== "PAID"):
    await bot.send_message(message.chat.id, text=f'⚠️{_("Оплата произведена", lang)}')
    await bot.send_sticker(message.chat.id, sticker='CAACAgUAAxkBAAEHvixj68fSmfjENkGT_VlvKXLsUGDn_gACeAcAAmwOeFW64xk-anTaKS4E',reply_markup=get_start_reply_keyboard(lang))
    await buy_message_id.delete()
    await bot.delete_message(money_sticker.chat.id, money_sticker.message_id)
    db.change_transaction_state(message.chat.id, 'closed')
    await ClientStates.main_state.set() # Установка состояния конечного автомата
    return 'success'
  else:
    return 'fail'

@dp.message_handler(state=ClientStates.price_list)
async def any_input_while_price_list_state(message: Message) -> None:
  lang = db.get_lang(message.from_user.id)  # Получение языка пользователя
  prices = db.get_price_list()
  for position in prices:
    if (message.text==_(position[1], lang)):
      await ClientStates.buy_subscription.set() # Установка состояния конечного автомата
      bill = p2p.bill(amount=position[2], lifetime=15, comment='')
      db.add_open_transaction(message.from_user.id, bill.bill_id, datetime.datetime.now())
      paylink_message = await message.answer(text=_(f'{bill.bill_id}', lang), reply_markup=get_p2p_inline_keyboard(bill.pay_url, lang))
      await message.delete()
      result_of_buying = await buying(paylink_message, bill.bill_id)
      if (result_of_buying == 'success'):
        db.add_subscription(message.from_user.id, position[0], datetime.datetime.now(), (datetime.datetime.now()+relativedelta(months=position[3])))
      return
  if (message.text==_('В главное меню', lang)):
    await ClientStates.main_state.set() # Установка состояния конечного автомата
    await message.answer(text=_('Возврат в <b>главное меню</b>', lang), reply_markup=get_start_reply_keyboard(lang))
  else:
    await message.answer(text=_('Некорректное действие', lang))
  await message.delete()

@dp.message_handler(state=ClientStates.buy_subscription)
async def any_input_while_buy_subscription_state(message: Message) -> None:
  lang = db.get_lang(message.from_user.id)  # Получение языка пользователя
  if (message.text==_('В главное меню', lang)):
    await ClientStates.main_state.set() # Установка состояния конечного автомата
    if db.get_open_transaction(message.from_user.id):
      db.change_transaction_state(message.from_user.id, 'withdrawn')
      await array_for_delete_messages[0].delete()
      await bot.delete_message(message.chat.id, array_for_delete_messages[1].message_id)
      await bot.send_message(message.from_user.id, text=f'⚠️{_("Оплата отменена", lang)}')
      await bot.send_sticker(message.from_user.id, sticker='CAACAgUAAxkBAAEHvkFj682KQHw0Qj9SnG2_SLS1z6SmBAACEwgAAscvcVV5yM6pt7RGHi4E')
    await message.answer(text=_('Возврат в <b>главное меню</b>', lang), reply_markup=get_start_reply_keyboard(lang))
    await message.delete()
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

@dp.errors_handler(exception=BotBlocked) # Обработка исключения, если пользователь заблокировал бота
async def error_bot_blocked_handler(update: Update, exception: BotBlocked):
  print('Бот остановлен или заблокирован!')
  return True