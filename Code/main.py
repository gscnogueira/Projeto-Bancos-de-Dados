#!/bin/python
import mysql.connector
import Entidades
import DAO
import copy
from datetime import date

if __name__ == '__main__':

    DAOPaciente = DAO.Paciente()
    DAOFisioterapeuta = DAO.Fisioterapeuta()
    DAOTelefone = DAO.Telefone()

    joao = Entidades.Paciente(
        'Marcelo rezende', '50405152000', date(2000, 9, 16), '71515030')

    dados = {
        'crefito':'123456F',
        # 'percent': 10,
        'nome':'Castro Alves',
        'cpf': '04827523193',
        'complemento':'zé lele',
        'dt_nasc':date(2001,9,11),
        'cep': '12345678',
    }
    marcos = Entidades.Fisioterapeuta(**dados);
    mercos = copy.copy(marcos)
    mercos.nome = "Marcos Castro"


    DAOFisioterapeuta.update(marcos, dt_nasc = date(2000,9,16))



