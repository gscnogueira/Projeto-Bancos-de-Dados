# python nao permite mais de um construtor
# funçao __str__ define como tratar o objeto como string
# olhar método __iter__
# metodo isinstance retorna se objeto é instancia de uma classe

from datetime import date


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
        if len(nome) > self.TAM_NOME:
            raise ValueError('O nome de uma pessoa  pode ter no máximo'
                             f' {self.TAM_NOME} caracteres')
        if not all(c.isalpha() or c.isspace() for c in nome):
            raise ValueError('O nome de uma pessoa deve ser composto'
                             ' apenas por caracteres alfabéticos')
        self._nome = nome

    @staticmethod
    def _valida_cpf(CPF):
        v1, v2 = [0, 0]
        for i in range(0, 9):
            v1 += int(CPF[i])*(9-(i % 10))
            v2 += int(CPF[i])*(9-((i+1) % 10))
        v1 %= 11
        v1 %= 10
        v2 += v1*9
        v2 %= 11
        v2 %= 10
        return int(CPF[-1]) == v1 and int(CPF[-2]) == v2

    @property
    def CPF(self):
        return self._CPF

    @CPF.setter
    def CPF(self, CPF):
        if len(CPF) != self.TAM_CPF:
            raise ValueError('O CPF deve possuir 11 digitos')
        if not CPF.isnumeric():
            raise ValueError('O CPF deve ser composto apenas por digitos')
        if not self._valida_cpf(CPF):
            raise ValueError('CPF inválido')
        self._CPF = CPF

    @property
    def dt_nasc(self):
        return self._dt_nasc

    @dt_nasc.setter
    def dt_nasc(self, dt):
        self._dt_nasc = dt

    @property
    def CEP(self):
        return self._CEP

    @CEP.setter
    def CEP(self, CEP):
        if len(CEP) != self.TAM_CEP:
            raise ValueError('CEP deve ter 8 digitos')
        self._CEP = CEP

    @property
    def complemento(self):
        return self._complemento

    @complemento.setter
    def complemento(self, complemento):
        if complemento != None and len(complemento) > self.TAM_COMPLEMENTO:
            raise ValueError('Complemento deve ter no máximo 60 caracteres')
        self._complemento = complemento

    def __init__(self, nome, cpf, dt_nasc, cep, complemento=None):
        self.CPF = cpf
        self.nome = nome
        self.dt_nasc = dt_nasc
        self.CEP = cep
        self.complemento = complemento


class Paciente(Pessoa):
    pass


class Fisioterapeuta(Pessoa):

    @property
    def percent_recebido(self):
        return self._percent_recebido

    @percent_recebido.setter
    def percent_recebido(self, percent):
        if (percent) and not (0 < percent <100):
            raise ValueError('Valor de percentual inválido')
        self._percent_recebido = percent

    @property
    def CREFITO(self):
        return self._CREFITO

    @CREFITO.setter
    def CREFITO(self, crefito):
        if len(crefito) != 7 :
            raise ValueError('CREFITO deve conter 7 caracteres')
        if not ( crefito[:-1] ).isnumeric():
            raise ValueError(
                'Os primeiros 6 caracteres de um CREFITO devem ser digitos')
        if crefito[-1] != 'F':
            raise ValueError('CREFITO informado contém último digito inválido')
        self._CREFITO = crefito

    def __init__(self,crefito, nome, cpf, dt_nasc, cep, complemento=None, percent = None):
        super().__init__(nome, cpf, dt_nasc, cep, complemento)
        self.percent_recebido = percent
        self.CREFITO = crefito


class Telefone:

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, numero):
        if len(numero) != 11 and len(numero) != 10:
            raise ValueError(
                'Numero de telefone deve ter entre 10 e 11 digitos')
        if not numero.isnumeric():
            raise ValueError(
                'Numero de telefone deve ser composto apenas por digitos')
        self._numero = numero
    

    def __init__(self,numero):
        self.numero = numero

