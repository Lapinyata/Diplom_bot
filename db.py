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

  def change_lang(self, user_id, lang): 
    with self.connection:
      self.cursor.execute("UPDATE users set lang = ? where user_id = ?",(lang, user_id,))

  def news_prediction_exists(self, user_id, news_text, true_prediction):
    with self.connection:
      result = self.cursor.execute("""WITH cte_1 as (SELECT * FROM user_news_predictions where user_id = ? and true_prediction = ?)
                                      SELECT * FROM cte_1 where news_text == ?""",(user_id, true_prediction, news_text,)).fetchall()
      return bool(len(result))

  def download_prediction_result(self, user_id, news_text, true_prediction):
    with self.connection:
      self.cursor.execute("INSERT INTO user_news_predictions (user_id, news_text, true_prediction) values(?, ?, ?)",(user_id, news_text, true_prediction,))

  def get_price_list(self):
    with self.connection:
      result = self.cursor.execute("SELECT id, name, price, months FROM price_list").fetchall()
      return result

  # def add_transactions(self, user_id, bill_id):  # Метод добавления пользователя в таблицу users
  #   with self.connection:
  #     return self.cursor.execute("INSERT INTO transactions (user_id, bill_id) values(?, ?)",(user_id, bill_id,))

  # def get_transactions(self, user_id):
  #   with self.connection:
  #     result = self.cursor.execute("SELECT * FROM transactions where user_id = ?",(user_id,)).fetchmany(1)
  #     return bool(len(result))

  # def delete_transactions(self, user_id):  # Метод удаления записи после успешной оплаты
  #   with self.connection:
  #     return self.cursor.execute("DELETE FROM transactions where user_id = ?",(user_id,))

  def add_open_transaction(self, user_id, bill_id, date):  # Метод добавления пользователя в таблицу users
    with self.connection:
      return self.cursor.execute("INSERT INTO transactions (user_id, bill_id, state, date) values(?, ?, ?, ?)",(user_id, bill_id, 'open', date,))

  def get_open_transaction(self, user_id):
    with self.connection:
      result = self.cursor.execute("SELECT * FROM transactions where user_id = ? and state = 'open'",(user_id,)).fetchmany(1)
      return bool(len(result))

  def change_transaction_state(self, user_id, state):  # Метод удаления записи после успешной оплаты
    with self.connection:
      return self.cursor.execute("UPDATE transactions set state = ? where user_id = ? and state = 'open'",(state, user_id,))

  def add_subscription(self, user_id, sub_id, start_date, end_date):
    with self.connection:
      return self.cursor.execute("INSERT INTO subscriptions (user_id, sub_id, start_date, end_date) values(?, ?, ?, ?)",(user_id, sub_id, start_date, end_date,))

  def get_subscription_info(self, user_id, cur_date):
    with self.connection:
      result = self.cursor.execute("SELECT end_date FROM subscriptions where user_id=? and end_date>?",(user_id, cur_date,)).fetchmany(1)
      return result