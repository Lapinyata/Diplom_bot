from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from translations import _

def get_start_reply_keyboard(lang) -> ReplyKeyboardMarkup:
  kb = ReplyKeyboardMarkup(resize_keyboard=True)
  button_1 = KeyboardButton(_('Сменить язык', lang))
  button_2 = KeyboardButton(_('Купить подписку', lang))
  button_3 = KeyboardButton(_('Начать работу', lang))
  kb.add(button_1,button_2).add(button_3)
  return kb

def get_finish_reply_keyboard(lang) -> ReplyKeyboardMarkup:
  kb = ReplyKeyboardMarkup(resize_keyboard=True)
  button_1 = KeyboardButton(_('Сменить язык', lang))
  button_2 = KeyboardButton(_('Купить подписку', lang))
  button_3 = KeyboardButton(_('Завершить работу', lang))
  kb.add(button_1,button_2).add(button_3)
  return kb

def get_lang_inline_keyboard() -> InlineKeyboardMarkup:
  kb = InlineKeyboardMarkup(row_width=2)
  button_1 = InlineKeyboardButton(text='Русский', callback_data='lang_ru')
  button_2 = InlineKeyboardButton(text='English', callback_data='lang_en')
  kb.add(button_1,button_2)
  return kb

def remove_reply_keyboard() -> ReplyKeyboardRemove:
  return ReplyKeyboardRemove()