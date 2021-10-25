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
            cursor.execute(
                f"insert into {self.TABLE} values (%s, %s, %s,%s,%s)",
                (paciente.CPF,
                 paciente.nome,
                 paciente.dt_nasc,
                 paciente.CEP,
                 paciente.complemento))
        except mysql.connector.Error as err:
            if(err.errno == errorcode.ER_DUP_ENTRY):
                print('CPF já registrado')
            else:
                print(err)
        finally:
            db.commit()
            cursor.close()

    def delete(self, paciente):
        cursor = db.cursor()
        try:
            cursor.execute(f"delete from {self.TABLE} where CPF = %s",
                           (paciente.CPF,))
        except mysql.connector.Error as err:
            print(err)
        finally:
            db.commit()
            cursor.close()

    def update(self, paciente, paciente_atualizado):
        cursor = db.cursor()
        op = (f"update {self.TABLE} set"
              " nome = %(_nome)s,"
              " CPF = %(_CPF)s,"
              " data_nasc  = %(_dt_nasc)s,"
              " CEP = %(_CEP)s,"
              " complemento = %(_complemento)s"
              " where CPF = '50405152000'")
        try:
            cursor.execute(op, paciente_atualizado.__dict__)
        except mysql.connector.Error as err:
            print(err)
        finally:
            db.commit()
            cursor.close()


class Fisioterapeuta:

    TABLE = 'Fisioterapeuta'

    def insert(self, fisio):
        cursor = db.cursor()
        colunas = [ff[1:] for (ff, ss) in
                   fisio.__dict__.items() if ss != None]
        values = [ss for (ff, ss) in
                   fisio.__dict__.items() if ss != None]

        placeholder = ','.join(len(colunas)*['%s'])

        op = (f"insert into {self.TABLE} "
              f"({','.join(colunas)}) "
              f"values({placeholder})")
        try:
            cursor.execute(op, tuple(values))
        except mysql.connector.Error as err:
            print(err)
        finally:
            db.commit()
            cursor.close()

    def delete(self, fisio):
        cursor = db.cursor()
        op = f'delete from {self.TABLE} where CREFITO = %s'
        try:
            cursor.execute(op, (fisio.CREFITO,))
        except mysql.connector.Error as err:
            print(err)
        finally:
            db.commit()
            cursor.close()

    def update(self, fisio, CREFITO=None, nome=None,
               dt_nasc=None, CEP=None, complemento=None,
               percent_recebido=None, CPF=None):

        params = [(ff, ss) for (ff, ss) in locals().items()
                   if ss != None][2:]

        columns = [tup[0] for tup in params]
        values = tuple([tup[1] for tup in params])

        placeholders = [column+' = %s' for column in columns]
        placeholders = ','.join(placeholders)
        print(placeholders)
        op = (f"update {self.TABLE} set " + placeholders
              +f" where CREFITO = '{fisio.CREFITO}'")
        print(op)

        cursor = db.cursor()
        try:
            cursor.execute(op,values)
        except mysql.connector.Error as err:
            print(err)
        finally:
            db.commit()
            cursor.close()


class Telefone:
    TABLE = 'TelefonePaciente'

    def insert_telefone_paciente(self, paciente, telefone):
        cursor = db.cursor()
        op = f"insert into {self.TABLE} values(%s,%s)"
        try:
            cursor.execute(op, (telefone.numero, paciente.CPF))
        except mysql.connector.Error as err:
            print(err)
        finally:
            db.commit()
            cursor.close()

    def get_telefones_paciente(self, paciente):
        cursor = db.cursor()
        op = ("select telefone from TelefonePaciente "
              "where Paciente_CPF = %s")
        try:
            cursor.execute(op, (paciente.CPF,))
            telefones = [tup[0] for tup in cursor]
        except mysql.connector.Error as err:
            print(e)
        finally:
            cursor.close()
        return telefones






