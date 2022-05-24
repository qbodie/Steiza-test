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

    def addUser(self, username, email, password):
        pass