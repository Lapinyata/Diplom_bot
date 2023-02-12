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
    'CAACAgIAAxkBAAEHqsRj5gntHgyhS50H9BvijKtAeEjh1wACuwIAAjrRBwABoYHYWwuDTsEuBA': 'CAACAgQAAxkBAAEHtMBj6QwIHKdwGYIo4I2XvN_vcFS7QgACPgYAAhXc8gJdj6lDzGWxCy4E'
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