import PySimpleGUI as sg
import Entidades
import DAO


class Paciente:
    DAOPaciente = DAO.Paciente()  
    def cadastro(self):
        layout = [[sg.Text("Preencha os campos a seguir")],
                  [sg.Text("Nome:")],
                  [sg.Input(key='nome')],
                  [sg.Text(size=(40, 1), k='err-nome')],
                  [sg.Text("Data de Nascimento:")],
                  [sg.Input(key='dt_nasc', default_text='dd/mm/aaaa')],
                  [sg.Text(size=(40, 1), k='err-dt_nasc')],
                  [sg.Text("CPF")],
                  [sg.Input(key='cpf')],
                  [sg.Text(size=(40, 1), k='err-cpf')],
                  [sg.Text("CEP")],
                  [sg.Input(key='cep')],
                  [sg.Text(size=(40, 1), k='err-cep')],
                  [sg.Text("Complemento")],
                  [sg.Input(key='complemento')],
                  [sg.Text(size=(40, 1), k='err-complemento')],
                  [sg.Button('Ok', bind_return_key=1), sg.Button('Cancelar')]
                  ]

        window = sg.Window('test', layout, location=(683, 384))

        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                break

            error_fields = ['err-cpf', 'err-nome', 'err-cep',
                            'err-complemento', 'err-dt_nasc']
            for item in error_fields:
                window[item].update('')
            is_okay = True
            paciente = Entidades.Paciente()
            try:
                paciente.CPF = values['cpf']
            except Entidades.CPFError as err:
                window['err-cpf'].update(err, text_color='red')
                is_okay &= 0
            try:
                paciente.nome = values['nome']
            except Entidades.NomeError as err:
                window['err-nome'].update(err, text_color='red')
                is_okay &= 0
            try:
                paciente.CEP = values['cep']
            except Entidades.CEPError as err:
                window['err-cep'].update(err, text_color='red')
                is_okay &= 0
            try:
                paciente.complemento = values['complemento']
            except Entidades.ComplementoError as err:
                window['err-complemento'].update(err, text_color='red')
                is_okay &= 0
            try:
                paciente.dt_nasc = values['dt_nasc']
            except Entidades.DataError as err:
                window['err-dt_nasc'].update(err, text_color='red')
                is_okay &= 0
            if is_okay:
                print(paciente.__dict__)
                self.DAOPaciente.insert(paciente)
                break

        window.close()


if __name__ == '__main__':
    ap = Paciente()
    ap.cadastro()
