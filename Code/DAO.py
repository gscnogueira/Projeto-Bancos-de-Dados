import Entidades
import mysql.connector
import config
from mysql.connector import errorcode

db = mysql.connector.connect(**config.login)


class Paciente:
    TABLE = 'Paciente'

    def insert(self, paciente):
        cursor = db.cursor()
        try:
            cursor.execute("insert into Paciente values (%s, %s, %s,%s,%s)", (paciente.CPF,
                                                                              paciente.nome, paciente.dt_nasc, paciente.CEP, paciente.complemento))
        except mysql.connector.Error as err:
            if(err.errno == errorcode.ER_DUP_ENTRY):
                print('CPF já registrado')
            else:
                print(err)
        finally:
            db.commit()
            cursor.close()



