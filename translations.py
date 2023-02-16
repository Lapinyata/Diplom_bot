translations = {
  'en': {
    'Здравствуйте': 'Hello',
    'Ваш Telegram ID': 'Your Telegram ID',
    'Отправь мне текст новости': 'Send me the news text',
    'Выбери язык': 'Choose lang',
    'Некорректный ввод': 'Incorrect input',
    'Новость является истинной с вероятностью': 'News is true with a probability of',
    'Новость является фейком с вероятностью': 'News is fake with a probability of',
    'Затрудняюсь определить, заслуживает ли полученная информация доверия': 'Find it difficult to determine whether the information received is trustworthy',
    'Это не текст новости!': 'This is not news text!',
    'Сменить язык': 'Change lang',
    'Купить подписку': 'Buy subscription',
    'Начать работу': 'Get started',
    'Завершить работу': 'Get finished',
    'Работа завершена': 'Work completed',
    'CAACAgIAAxkBAAEHqsRj5gntHgyhS50H9BvijKtAeEjh1wACuwIAAjrRBwABoYHYWwuDTsEuBA': 'CAACAgQAAxkBAAEHtMBj6QwIHKdwGYIo4I2XvN_vcFS7QgACPgYAAhXc8gJdj6lDzGWxCy4E',
    'Выбран раздел: <b>Купить подписку</b>': 'Selected section: <b>Buy a subscription</b>',
    'Пожалуйста, ознакомьтесь с прейскурантом': 'Please see the price list',
    'Подписка на месяц': 'monthly subscription',
    'Подписка на 3 месяца': '3-month subscription',
    'Подписка на 6 месяцев': '6-month subscription',
    'Подписка на год': 'annual subscription',
    'В главное меню': 'Back to main menu',
    'Ссылка для оплаты (действительна 15 минут)': 'Payment link (valid for 15 minutes)',
    'Оплатить': 'Go to pay',
    'Возврат в <b>главное меню</b>': 'Returned to <b>main menu</b>',
    'Оплата произведена': 'Payment completed',
    'Оплата отменена': 'Payment withdrawn',
    'Текущий статус подписки': 'Current subscription state',
    'Активна до': 'Active utill',
    'Неактивна': 'Not active',
    'Полученная новость содержит более 1500 символов!': 'Received news contains more than 1500 characters!',
    '<b>Купите подписку</b>, чтобы обрабатывать новости любого размера': '<b>Buy a subscription</b> to process any size news'
    #'₽': '$'
  }
}

def _(text, lang='ru'):
  if lang == 'ru':
    return text
  else: 
    global translations
    try:
      return translations[lang][text]
    except:
      return text