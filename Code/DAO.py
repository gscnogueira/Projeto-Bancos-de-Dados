import Entidades
import mysql.connector
import config
from mysql.connector import errorcode
from datetime import date

db = mysql.connector.connect(**config.login)


class Horario:
    def get_id_horario(self, horario):
        cursor = db.cursor()
        op = ("select id_Horario "
              "from Horario where tempo_inicio = %s")
        try:
            cursor.execute(op, (horario,))
            return cursor.fetchone()[0]

        except mysql.connector.Error as err:
            print(err)
        finally:
            cursor.close()
    def lista_horarios(self):
        cursor = db.cursor()
        op = ("select tempo_inicio "
              "from Horario")
        try:
            cursor.execute(op)
            return cursor.fetchall()

        except mysql.connector.Error as err:
            print(err)
        finally:
            cursor.close()

class Box:
    def list_boxes(self):
        cursor = db.cursor()
        op = ("select * from Box ")
        try:
            cursor.execute(op)
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        finally:
            cursor.close()

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
                raise ValueError("CPF já está cadastrado")
            else:
                raise Exception("Erro no aceso à base de dados")
        finally:
            db.commit()
            cursor.close()

    def delete(self, cpf):
        cursor = db.cursor()
        try:
            cursor.execute(f"delete from {self.TABLE} where CPF = %s",
                           (cpf,))
        except mysql.connector.Error as err:
            print(err)
        finally:
            db.commit()
            cursor.close()

    def update(self, cpf, paciente_atualizado):
        cursor = db.cursor()
        op = (f"update {self.TABLE} set"
              " nome = %(_nome)s,"
              " CPF = %(_CPF)s,"
              " data_nasc  = %(_dt_nasc)s,"
              " CEP = %(_CEP)s,"
              " complemento = %(_complemento)s"
              " where CPF = '{}'".format(cpf))
        try:
            cursor.execute(op, paciente_atualizado.__dict__)
        except mysql.connector.Error as err:
            if(err.errno == errorcode.ER_DUP_ENTRY):
                raise ValueError("CPF já está cadastrado")
            else:
                raise Exception("Erro no aceso à base de dados")
        finally:
            db.commit()
            cursor.close()

    def list(self):
        cursor = db.cursor()
        op = ("select cpf, nome from Paciente "
              "order by nome")
        try:
            cursor.execute(op)
            return [x for x in cursor]
        except mysql.connector.Error as err:
            print(err)

    def dados(self, cpf):
        cursor = db.cursor(dictionary=True)
        op = ("select * from Paciente "
              "where CPF = %s")
        try:
            cursor.execute(op, ( cpf, ))
            return next(cursor)
        except mysql.connector.Error as err:
            print(err)
        finally:
            cursor.close()


    def get_planos_de_saude(self, cpf):
        cursor = db.cursor()
        op = ("select razao_social, id_plano_paciente from "
              " (PlanoDeSaude join Paciente_has_PlanoDeSaude"
              "  on id = PlanoDeSaude_id)"
              "where Paciente_CPF = %s")
        try:
            cursor.execute(op, (cpf,))
            return [' - '.join(x[0:2] ) for x in cursor.fetchall() if x]
        except mysql.connector.Error as er:
            print(err)
        finally:
            cursor.close()

    def get_id_plano(self, cpf, nome_plano):
        cursor = db.cursor()
        op = ("select id from "
              "(Paciente_has_PlanoDeSaude join PlanoDeSaude on PlanoDeSaude_id = id)"
              "where Paciente_CPF = %s and razao_social = %s")
        try:
            cursor.execute(op, ( cpf, nome_plano ))
            return cursor.fetchone()[0]
        except mysql.connector.Error as er:
            print(err)
        finally:
            cursor.close()


class Sessao:
    def get_sessoes_paciente(self, cpf, date, id_horario ):
        cursor = db.cursor(dictionary = True)
        op = ( "select * from VInfoSessao where"
               "(Paciente_CPF = %s and data_sessao = %s and id_Horario = %s )"
               " order by data_sessao desc")
        try:
            cursor.execute(op, (cpf,date, id_horario,))
            return cursor.fetchall()[0]
        except mysql.connector.Error as err:
            print(err)
        finally:
            cursor.close()

    def get_horario_sessoes_paciente(self, cpf):
        cursor = db.cursor()
        op =( "select data_sessao, tempo_inicio from VInfoSessao where Paciente_CPF = %s"
              " order by data_sessao desc")
        try:
            cursor.execute(op, (cpf,))
            # return [x[0].strftime("%d/%m/%Y") + ' - ' +str(x[1]) for x in cursor if x]
            return [x for x in cursor]
        except mysql.connector.Error as err:
            print(err)
        finally:
            cursor.close()
    def get_doencas(self, cpf, date, id_horario ):
        cursor = db.cursor()
        op = ( "select CID, descricao from"
               " Sessao_trata_Doenca natural join Doenca"
               " where (Paciente_CPF = %s and data_sessao = %s and id_Horario = %s)");
        try:
            cursor.execute(op, (cpf,date, id_horario,))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            print(err)
        finally:
            cursor.close()
    def get_procedimentos_sessao(self, cpf, id_horario, data, id_plano ):
        cursor = db.cursor(buffered = True)
        try:
                cursor.callproc('procedimentos_sessao',
                                (cpf, id_horario, data, id_plano))
                return next(cursor.stored_results()).fetchall()
        except mysql.connector.Error as err:
            print(err)
        finally:
            cursor.close()

    def insert(self, sessao):
        cursor = db.cursor()
        op = ("insert into Sessao values("
              " %(id_Horario)s,"
              " %(id_DiaSemana)s,"
              " %(_data_sessao)s,"
              " %(idBox)s,"
              " %(Paciente_CPF)s,"
              " %(particular)s,"
              " %(id_PlanoDeSaude)s,"
              " %(observacoes)s)"
              )
        try:
            cursor.execute(op, sessao.__dict__)
        except mysql.connector.Error as err:
            if(err.errno == errorcode.ER_DUP_ENTRY):
                print(err)
                raise ValueError("Dados em conflito com sessão já cadastrada")
            else:
                raise Exception("Erro no aceso à base de dados")
        finally:
            db.commit()
            cursor.close()








