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
        v1%=11; v1%=10
        v2+=v1*9; v2%=11; v2%=10
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
        if len(CEP)!=self.TAM_CEP:
            raise ValueError('CEP deve ter 8 digitos')
        self._CEP = CEP

    @property
    def complemento(self):
        return self._complemento

    @complemento.setter
    def complemento(self, complemento):
        if complemento != None and len(complemento)>self.TAM_COMPLEMENTO:
            raise ValueError('Complemento deve ter no máximo 60 caracteres')
        self._complemento = complemento

    def __init__(self, nome, cpf, dt_nasc, cep, complemento = None):
        self.CPF = cpf
        self.nome = nome
        self.dt_nasc = dt_nasc
        self.CEP = cep
        self.complemento = complemento

        
class Paciente(Pessoa):
    pass;





if __name__ == '__main__':

    hominho = Paciente()
    hominho.nome = 'Marcelo Corvino Nogueira'
    hominho.CPF = '20009491856'
    hominho.dt_nascimento = date(1972,6,19)
    hominho.CEP = '71515030'
    hominho.complemento = ''
