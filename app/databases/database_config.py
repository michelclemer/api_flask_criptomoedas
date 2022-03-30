import mysql.connector

class DatabaseConnection:
    def __init__(self):
        pass

    def start_db(self):
        cnx = mysql.connector.connect(user='newuser', password='password',
                                      host='localhost',
                                      database='candles')

        return cnx

    def create_table(self):
        conn = self.start_db()
        cursor = conn.cursor()
        try:
            cursor.execute('DROP TABLE IF EXISTS candles;')

            sql = '''CREATE TABLE candles(
               id serial PRIMARY KEY,
               moeda VARCHAR(150) NOT NULL,
               periodicidade integer NOT NULL,
               open VARCHAR(150) NOT NULL,
               low VARCHAR(150) NOT NULL,
               high VARCHAR(150) NOT NULL,
               close VARCHAR(150) NOT NULL,
               hash VARCHAR(150) NOT NULL
                )'''
            cursor.execute(sql)
            conn.commit()
            print("Tabela criada!!")
        except Exception as a:
            print("Erro ao criar tabela")
            print(a)
            pass
        cursor.close()
        conn.close()
        return

    def insert_candle(self, lista: dict):
        conn = self.start_db()

        sql = ('INSERT INTO `candles` (`moeda`, `periodicidade`, `open`, `low`, `high`, `close`, `hash`) VALUES (%s, %s, %s, %s, %s, %s, %s)')
        val = (lista['moeda'], lista['periodicidade'], lista['open'], lista['low'], lista['high'], lista['close'], lista['hash'])

        with conn.cursor() as cursor:
            cursor.execute(sql, val)
            conn.commit()
            print("Inserido ok")
        conn.close()

