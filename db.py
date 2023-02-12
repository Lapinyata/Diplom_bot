import sqlite3

class Database:
  def __init__(self, db_file):
    self.connection = sqlite3.connect(db_file)  # Подключение к БД 
    self.cursor = self.connection.cursor()  # Курсор, предоставляющий инструментарий для взаимодействия с БД

  def user_exists(self, user_id): # Метод проверки наличия пользователя в таблице users
    with self.connection:
      result = self.cursor.execute("SELECT * FROM users where user_id = ?",(user_id,)).fetchall() # Делаем выбоку строк по user_id
      return bool(len(result))  # Так как user_id уникален, нам возвращается либо одна строка, либо ни одной (переводим это число в булевый тип)
  
  def add_user(self, user_id, username, lang):  # Метод добавления пользователя в таблицу users
    with self.connection:
      return self.cursor.execute("INSERT INTO users (user_id, username, lang) values(?, ?, ?)",(user_id, username, lang,))

  def get_lang(self, user_id):  # Метод получения lang пользоователя из таблицы users
    with self.connection:
      return self.cursor.execute("SELECT lang FROM users where user_id = ?",(user_id,)).fetchone()[0]

  def change_lang(self, user_id, lang):  # Метод получения lang пользоователя из таблицы users
    with self.connection:
      self.cursor.execute("UPDATE users set lang = ? where user_id = ?",(lang, user_id,))