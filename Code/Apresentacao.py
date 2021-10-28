import PySimpleGUI as sg
import Entidades
from datetime import date
import DAO


def consulta_dict(dic,key):
    try:
        v = dic[key]
        if isinstance(v,date):
            v = v.strftime("%d/%m/%Y")

        return v
    except Exception:
        return ''
def freeze(window):
    for e in window.element_list():
        if isinstance(e, (sg.Button,sg.Listbox, ) ):
            e.update(disabled = True)

def unfreeze(window):
    for e in window.element_list():
        if isinstance(e, (sg.Button,sg.Listbox, ) ):
            e.update(disabled = False)

def confirmar_acao(mensagem="Deseja prosseguir com essa operação?"):
    layout = [[sg.Text(mensagem)],
              [sg.Button("Sim", expand_x=True),
               sg.Button("Não", expand_x=True)]]

    window = sg.Window("Confirme a operação", layout,
                       text_justification='center',
                       keep_on_top=True)

    event, values = window.read()

    window.close()

    return event == 'Sim'


class Paciente:
    DAO = DAO.Paciente()

    def cadastro(self, cpf_existente = None):
        dados = {}
        if(cpf_existente):
            dados =  self.DAO.dados(cpf_existente)

        layout = [[sg.Text("Preencha os campos a seguir")],
                  [sg.Text("Nome:")],
                  [sg.Input(key='nome',
                            default_text = consulta_dict(dados, 'nome'))],
                  [sg.Text(size=(40, 1), k='err-nome')],
                  [sg.Text("Data de Nascimento:")],
                  [sg.Input(key='dt_nasc',
                            default_text=consulta_dict(dados, 'data_nasc'))],
                  [sg.Text(size=(40, 1), k='err-dt_nasc')],
                  [sg.Text("CPF")],
                  [sg.Input(key='cpf',
                            default_text = consulta_dict(dados,'CPF'))],
                  [sg.Text(size=(40, 1), k='err-cpf')],
                  [sg.Text("CEP")],
                  [sg.Input(key='cep',
                            default_text = consulta_dict(dados, 'CEP'))],
                  [sg.Text(size=(40, 1), k='err-cep')],
                  [sg.Text("Complemento")],
                  [sg.Input(key='complemento',
                            default_text = consulta_dict(dados,'complemento'))],
                  [sg.Text(size=(40, 1), k='err-complemento')],
                  [sg.Button('Ok', bind_return_key=1),
                   sg.Button('Cancelar')]
                  ]

        window = sg.Window('test', layout)

        cancelou = False
        while True:
            event, values = window.read()

            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                cancelou = True
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

                if cpf_existente:
                    self.DAO.update(cpf_existente,paciente)
                else:
                    self.DAO.insert(paciente)
                break

        window.close()
        return not cancelou

    def _lista_pacientes(self):
        lista = [(cpf, nome) for cpf, nome in
                 self.DAO.list()]
        lista = [' - '.join(e) for e in lista]
        return lista

    def display(self):

        paciente_column = [[sg.Listbox(values=self._lista_pacientes(),
                                       size=(60, 20),
                                       k="-LIST-",
                                       horizontal_scroll=True,
                                       enable_events=True)],
                           [sg.Button("Adicionar Paciente",
                                      expand_x = True,
                                      k = "-ADD-")]]

        dados_column = [[sg.Text("Selecione um paciente",
                                 size=(60, 1),
                                 justification='center',
                                 k="-TXT-")],
                        [sg.Text(k="-NOME-", size=(60, 1))],
                        [sg.Text(k="-CPF-", size=(60, 1))],
                        [sg.Text(k="-DATE-", size=(60, 1))],
                        [sg.Text(k="-CEP-", size=(60, 1))],
                        [sg.Text(k="-COMP-", size=(60, 1))],
                        [sg.Button("Atualizar",
                                   k="-UPD-",
                                   visible=False,
                                   disabled=True,
                                   # size = (10,1),
                                   expand_x=True),
                         sg.Button("Deletar",
                                   k="-DEL-",
                                   visible=False,
                                   disabled=True,
                                   # size = (10,1),
                                   expand_x=True)]
                        ]

        layout = [[sg.Column(paciente_column),
                   sg.VSeparator(),
                   sg.Column(dados_column)],
                  [sg.Button("Sair", k = "-CANCEL-" )]]
        window = sg.Window("Consulta Paciente", layout)

        cpf = ''
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == '-CANCEL-':
                break

            elif event == "-LIST-":
                selecionado = values["-LIST-"][0].split(' - ')
                cpf = selecionado[0]
                paciente = self.DAO.dados(cpf)
                window['-TXT-'].update('')
                window['-NOME-'].update(
                    "Nome: {}".format(paciente['nome']))
                window['-CPF-'].update(
                    "CPF: {}".format(paciente['CPF']))
                window['-DATE-'].update(
                    "Data de Nascimento: {}".format(paciente['data_nasc'].strftime("%d/%m/%Y")))
                window['-CEP-'].update(
                    "CEP: {}".format(paciente['CEP']))
                window['-COMP-'].update('')
                if (paciente['complemento']):
                    window['-COMP-'].update(
                        "Complemento: {}".format(paciente['complemento']))
                window['-DEL-'].update(disabled=False,
                                       visible=True)
                window['-UPD-'].update(disabled=False,
                                       visible=True)

            elif event == '-DEL-':


                freeze(window)
                if confirmar_acao():

                    self.DAO.delete(cpf)
                    window['-LIST-'].update(self._lista_pacientes(), disabled = False)
                    window['-TXT-'].update("Selecione um paciente")
                    window['-NOME-'].update('')
                    window['-CPF-'].update('')
                    window['-DATE-'].update('')
                    window['-CEP-'].update('')
                    window['-COMP-'].update('')
                    window['-DEL-'].update(visible = False)
                    window['-UPD-'].update(visible = False)


                unfreeze(window)


            elif event == '-ADD-':
                freeze(window)
                self.cadastro()
                unfreeze(window)
                window['-LIST-'].update(self._lista_pacientes())

            elif event == '-UPD-':
                freeze(window)
                if(cpf and self.cadastro(cpf)):
                    unfreeze(window)
                    window['-LIST-'].update(self._lista_pacientes())
                    window['-TXT-'].update("Selecione um paciente")
                    window['-NOME-'].update('')
                    window['-CPF-'].update('')
                    window['-DATE-'].update('')
                    window['-CEP-'].update('')
                    window['-COMP-'].update('')
                    window['-DEL-'].update(visible = False)
                    window['-UPD-'].update(visible = False)
                else:
                    unfreeze(window)
                
            

        window.close()


def menu_inicial():
    layout = [[sg.Text("Sistema Gerenciador de Clínicas", font = "Helvetica 26 bold")],
              [sg.Button("Pacientes", expand_x=True, k = '-PAC-'  )],
              [sg.Button("Funcionários", expand_x=True  )],
              [sg.Button("Planos de Saúde", expand_x=True  )],
              [sg.Button("Sessões", expand_x=True  )],
              [sg.Button("Sair", expand_x=True, k = '-QUIT-'  )]
              ]
    window = sg.Window("Sistema Gerenciador de Clínicas", layout,
                       text_justification = 'center')


    while True:

        event, values = window.read()

        freeze(window)
        if  event == '-QUIT-':
            break
        if event == '-PAC-':
            ap = Paciente()
            ap.display()

        unfreeze(window)


    window.close()

if __name__ == '__main__':
    menu_inicial()
