import mysql.connector

print("db file")
class DatabaseConnection:

    """
        Gerenciamento do banco de dados
    """

    def __init__(self):
        pass

    """ inicia o banco de dados  """
    def start_db(self)  -> dict:

        """
        Iniciar
        :return: connector
        """

        cnx = mysql.connector.connect(user='newuser', password='password',
                                      host='db',
                                      database='candles')

        return cnx

    """ Cria uma nova tabela """
    def create_table(self) -> None:
        """
        Criar
        :return: None
        """
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
               hash VARCHAR(150) NOT NULL,
               date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    """ Insere um novo candle ao banco de dados """
    def insert_candle(self, lista: dict) -> None:
        """
        Inserir
        :param lista:
        :return: None
        """
        conn = self.start_db()

        sql = ('INSERT INTO `candles` (`moeda`, `periodicidade`, `open`, `low`, `high`, `close`, `hash`) VALUES (%s, %s, %s, %s, %s, %s, %s)')
        val = (lista['moeda'], lista['periodicidade'], lista['open'], lista['low'], lista['high'], lista['close'], lista['hash'])

        with conn.cursor() as cursor:
            cursor.execute(sql, val)
            conn.commit()
        conn.close()

