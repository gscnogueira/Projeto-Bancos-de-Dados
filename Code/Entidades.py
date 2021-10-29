# python nao permite mais de um construtor
# funçao __str__ define como tratar o objeto como string
# olhar método __iter__
# metodo isinstance retorna se objeto é instancia de uma classe

from datetime import date

class CPFError(ValueError):
    def __init__(self, message = 'CPF inválido'):
        self.message = message
        super().__init__(self.message)


class NomeError(ValueError):
    def __init__(self, message = 'Nome inválido'):
        self.message = message
        super().__init__(self.message)


class CEPError(ValueError):
    def __init__(self, message = 'CEP inválido'):
        self.message = message
        super().__init__(self.message)

class DataError(ValueError):
    def __init__(self, message = 'Data inválida'):
        self.message = message
        super().__init__(self.message)

class ComplementoError(ValueError):
    def __init__(self, message = 'Complemento inválido'):
        self.message = message
        super().__init__(self.message)

class Pessoa:

    TAM_NOME = 100
    TAM_CPF = 11
    TAM_CEP = 8
    TAM_COMPLEMENTO = 60

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        nome = nome.upper()
        if len(nome) > self.TAM_NOME:
            raise NomeError()
        if not len(nome):
            raise NomeError
        if nome.isspace():
            raise NomeError
        if not all(c.isalpha() or c.isspace() for c in nome):
            raise NomeError()
        self._nome = nome

    @staticmethod
    def _valida_cpf(CPF):
        v1, v2 = [0, 0]
        for i in range (0,9):
            v1 +=int( CPF[i] )*(10-i)
            v2 +=int( CPF[i] )*(11-i)
        v1 = ((v1*10)%11)%10
        v2+=2*v1
        v2 = ((v2*10)%11)%10
        return int(CPF[-2]) == v1 and int(CPF[-1]) == v2

    @property
    def CPF(self):
        return self._CPF

    @CPF.setter
    def CPF(self, CPF):
        if len(CPF) != self.TAM_CPF:
            raise CPFError()
        if not CPF.isnumeric():
            raise CPFError()
        if not self._valida_cpf(CPF):
            raise CPFError()
        self._CPF = CPF

    @property
    def dt_nasc(self):
        return self._dt_nasc

    @dt_nasc.setter
    def dt_nasc(self, dt):
        dt = dt.split('/')
        if len(dt) != 3:
            raise DataError
        if not all(x.isnumeric() for x in dt):
            raise DataError
        dt = [int(x) for x in dt]
        try:
            data = date(dt[2], dt[1],dt[0])
            self._dt_nasc = data
        except Exception :
            raise DataError


    @property
    def CEP(self):
        return self._CEP

    @CEP.setter
    def CEP(self, CEP):
        if len(CEP) != self.TAM_CEP:
            raise CEPError()
        self._CEP = CEP

    @property
    def complemento(self):
        return self._complemento

    @complemento.setter
    def complemento(self, complemento):
        if complemento != None and len(complemento) > self.TAM_COMPLEMENTO:
            raise ComplementoError()
        if complemento.isspace():
            raise ComplementoError()
        if complemento.isspace() or not len(complemento):
            self._complemento = None
        else:
            self._complemento = complemento


class Paciente(Pessoa):
    pass

class Sessao:

    @property
    def data_sessao(self):
        return self._data_sessao;
    
    @data_sessao.setter
    def data_sessao(self, dt):
        dt = dt.split('/')
        if len(dt) != 3:
            raise DataError
        if not all(x.isnumeric() for x in dt):
            raise DataError
        dt = [int(x) for x in dt]
        try:
            data = date(dt[2], dt[1],dt[0])
            if data.weekday()>4:
                raise DataError('Não há atendimentos na data escolhida')
            self._data_sessao = data
        except Exception :
            raise DataError








