import sqlite3


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getUser(self):
        sql = '''SELECT * FROM contacts'''
        try:
            self.__cur.execute(sql)
            response = self.__cur.fetchall()
            if response:
                return response
        except:
            print('Ошибка чтения БД')

    def addUser(self, username, email, hpsw):
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM contacts WHERE email LIKE '{email}'")
            response = self.__cur.fetchone()
            if response['count'] > 0:
                print('Пользователь с таким email уже зарегестрирован.')
                return False

            self.__cur.execute("INSERT INTO contacts VALUES(NULL, ?, ?, ?)", (username, email, hpsw))
            self.__db.commit()
        except sqlite3.Error as e:
            print(str(e))
            return False
        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM contacts WHERE id = {user_id} LIMIT 1")
            response = self.__cur.fetchone()
            if not response:
                print('Пользватель не найден.')
                return False

            return response
        except sqlite3.Error as e:
            print(str(e))

        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM contacts WHERE email = '{email}' LIMIT 1")
            response = self.__cur.fetchone()
            if not response:
                print('Пользователь не найден')
                return False
            return response
        except sqlite3.Error as e:
            print(str(e))

        return False

    def addInput(self, name, lastname):
        try:
            self.__cur.execute("INSERT INTO inputs VALUES(NULL, ?, ?)", (name, lastname))
            self.__db.commit()
        except sqlite3.Error as e:
            print(str(e))
            return False
        return True
