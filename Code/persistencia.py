import mysql.connector
import Entidades
import DAO
from datetime import date

if __name__ == '__main__':
    joao = Entidades.Paciente('Marcelo rezende', '50405152000', date(2000, 9, 16),'71515030')
    DAOPaciente = DAO.Paciente()
    DAOPaciente.insert(joao)

