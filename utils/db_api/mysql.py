import datetime
import sqlite3


class MySqlDatabase:
    """
    Класс поддерживает следющие методы:

    .get_all_workouts(id_, start_date=None, end_date=None) -
     возвращает записи всех тренировок спортсмена по его id_,
      начиная со start_date и заканчивая end_date включительно.

    .get_name(id_) - возвращает имя спорсмена по его id_

    .add_workout(id_, workout, date) - добавляет запись тренировки в таблицу
     (id_ это идентификатор спорсмена)

    .add_sportsman(id_, name) - добавляет спорсмена в таблицу

    .update_name(id_, name) - обновляет имя спорсмена

    """
    def __init__(self, host, user, password, database):
        self.connection = sqlite3.connect(host)

    def __del__(self):
        self.connection.close()

    def get_all_workouts(self, id_, start_date=None, end_date=None):
        cursor = self.connection.cursor()
        query = "SELECT date, workout FROM workout WHERE telegram_id=?"
        params = (id_,)
        if start_date:
            query += " AND date >= ?"
            params += (start_date,)
        if end_date:
            query += " AND date <= ?"
            params += (end_date,)
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        # TODO date преобразовать в datetime (наверно)
        return result

    def get_name(self, id_):
        cursor = self.connection.cursor()
        query = "SELECT sportsman_name FROM users WHERE telegram_id=?"
        params = (id_,)
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def add_workout(self, id_, workout, date):
        cursor = self.connection.cursor()
        # TODO date наверно нужно преобразовать в строку
        query = "INSERT INTO workout (telegram_id, date, workout) VALUES (?, ?, ?)"
        params = (id_, date, workout)
        cursor.execute(query, params)
        self.connection.commit()
        cursor.close()

    def add_sportsman(self, id_, name):
        cursor = self.connection.cursor()
        query = "INSERT INTO users (telegram_id, sportsman_name) VALUES (?, ?)"
        params = (id_, name)
        cursor.execute(query, params)
        self.connection.commit()
        cursor.close()

    def update_name(self, id_, name):
        cursor = self.connection.cursor()
        query = "UPDATE users SET sportsman_name=? WHERE telegram_id=?"
        params = (name, id_)
        cursor.execute(query, params)
        self.connection.commit()
        cursor.close()


# tests
if __name__ == '__main__':
    db = MySqlDatabase(
        host='data/sportsmen_bot.db',
        user='',
        password='',
        database=''
    )
    db.add_sportsman(id_=12345, name='Maksim')
    assert db.get_name(id_=12345) == 'Maksim'
    db.update_name(id_=12345, name='Kirill')
    assert db.get_name(id_=12345) == 'Kirill'
    db.add_workout(id_=12345, workout='99 подтягиваний', date=datetime.date(year=2023, month=4, day=1))
    print(datetime.date(year=2023, month=4, day=1), '99 подтягиваний')
