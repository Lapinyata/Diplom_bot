import re
import nltk
from nltk.corpus import stopwords
from string import punctuation

nltk.download("stopwords")

def replace_datetime(text):
  re_min_sec = r'(0[6-9]|[0-5]\d)'     # Регулярное выражение для минут и секунд
  re_hour = r'(0|1)\d?|2[0-3]'         # Регулярное выражение для часов
  re_time = rf'({re_hour})(:{re_min_sec}){{1,2}}'  # Единое регулярное выражение для времени формата "часы:минуты:секунды"
  re_day = r'([0-2]?\d|3[01])'          # Регулярное выражение для дней 
  re_month = r'(0?\d|1[12])'            # Регулярное выражение для месяцев 
  re_eng_month = r'(jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)'   # Регулярные выражения для месяцев текстом
  re_rus_month = r'(январ(ь|я)|феврал(ь|я)|март(а)|апрел(ь|я)|ма(й|я)|июн(ь|я)|июл(ь|я)|август(а)|сентяьр(ь|я)|октябр(ь|я)|ноябр(ь|я)|декабр(ь|я))'
  date_patterns = {                     # Шаблоны разных форматов для поиска даты и времени
      'yyyy(-|по)yyyy': r'\d{4}( *(по|-|до) *)\d{4}',
      '20-го сентября 2010 года в 10:10:10': rf'{re_day}(-?о?(е|го))? +{re_rus_month}( +\d{4}( +(года|г\.?))?)?( +(с|к|в|на|,)? +{re_time})?',
      '20-th of september 2010 at 10:10:10': rf'{re_day}(-?th)? +(of +)?{re_eng_month}( +\d{4})?( +at +{re_time})?',
      'yyyy-mm[-dd]': rf'\d{{4}}-{re_month}(-{re_day})?',
      'dd-mm-yyyy': rf'{re_day}-{re_month}-\d{{4}}',
      'hh:mm:ss': re_time,
      'mm/dd/yyyy': rf'{re_month}/{re_day}/(\d\d){{1,2}}',
      'dd.mm.yyyy': rf'{re_day}\.{re_month}\.(\d\d){{1,2}}',
  }
  for pattern in date_patterns.values():  # Заменяем все найденные шаблоны на DATETIME
      text = re.sub(pattern, ' DATETIME ', text)
  return text

def special_tokenize(text):
    re_digit_symbols = r'\%/\$№€#₽£¥\*\+×∼℃°→\^∞÷'
    re_integer = r'\d[ \'\d]*'
    re_float = rf'{re_integer}[,\./]{re_integer}'
    patterns = {
        '<URL>': r'(https? ?: ?//)?[a-zA-Z0-9\./\?:@_=#-]+\.[a-zA-Z]{2,6}[a-zA-Z0-9\.&%/\?:@_=#-]*',
        '<NUM>': rf'[{re_digit_symbols} ]*({re_float}|{re_integer})[{re_digit_symbols} ]*',
    }
    for token, pattern in patterns.items():
        text = re.sub(pattern, f' {token} ', text)
    return text

def clean_text(text):
  text = replace_datetime(text)
  text = special_tokenize(text)
  text = re.sub(r'[^\w\s\d]', '',text)  # Удаление пунктуации
  text = re.sub(r'\s+', ' ',text)        # Замена нескольких пробелов на один
  text = re.sub(r'^\s+|\s+?$', '',text)  # Удаление начальных и конечных пробелов
  text = text.replace('ё','е').replace('Ё', 'Е') # Замена "ё" на "е"
  text = text.replace('\n', '')           # Удаление '\n'
  return text

def main_cleaner(message):
  clear_text = clean_text(message)
  russian_stopwords = stopwords.words("russian")
  clear_text = clear_text.lower()
  clear_text = clear_text.split(' ')
  tokens_of_text = lambda x: [token for token in x if (token not in russian_stopwords and token != " " and token.strip() not in punctuation)]
  clear_text = ' '.join(tokens_of_text(clear_text))
  return clear_text