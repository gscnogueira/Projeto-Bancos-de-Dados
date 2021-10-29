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


class Sessao:
    DAOSessao = DAO.Sessao()
    DAOPaciente = DAO.Paciente()
    DAOHorario = DAO.Horario()
    DAOBox = DAO.Box()
    def _gera_linhas(self, valores):
        return [v1 + ' - ' + v2
                for (v1, v2) in valores]
    def display_sessao(self,cpf, data, id_horario):

        dados = self.DAOSessao.get_sessoes_paciente(cpf,data, id_horario)
        doencas = self.DAOSessao.get_doencas(cpf, data, id_horario)
        procedimentos = self.DAOSessao.get_procedimentos_sessao(cpf,
                                                                id_horario,
                                                                data,
                                                                dados['PlanoDeSaude_id'])

        layout = [[sg.Text("Paciente: {}".format(dados['Paciente_nome']))],
                  [sg.Text("Fisioterapeuta: {}".format(dados['Fisioterapeuta_nome']))],
                  [sg.Text("Data: {}".format(dados['data_sessao'].strftime("%d/%m/%Y")))],
                  [sg.Text("Horario: {}".format(dados['tempo_inicio']))],
                  [sg.Text("Box: {}".format(dados['idBox']))],
                  [sg.Text("Plano de Saúde: {}".format(dados['PlanoDeSaude_nome']
                                                       if dados['PlanoDeSaude_nome']
                                                       else 'Consulta particular'))],
                  [sg.Text("Doenças Tratadas:", size = (30,1)),
                   sg.Text("   Procedimentos Realizados:", size = (30,1))],
                  [sg.Listbox(k='-DOENCAS-',
                              values = self._gera_linhas(doencas),
                              size = (30, 3),
                              horizontal_scroll = True),
                   sg.Listbox(k='-PROCS-',
                              values = self._gera_linhas(procedimentos),
                              size = (30, 3),
                              horizontal_scroll = True),
                   ],
                  [sg.Text("Observações:")],
                  [sg.Text(dados['observacoes']
                           if dados['observacoes']
                           else "",
                           size = (60,5),
                           text_color = 'black',
                           background_color = 'white')],
                  [sg.Button("Atualizar Dados", expand_x = True)],
                  [sg.Button("Sair", expand_x = True)]]

        window = sg.Window("Dados da Sessão", layout)
        event, values = window.read()
        window.close()

    def cadastro(self, cpf=None):
        horarios = self.DAOHorario.lista_horarios()
        boxes = self.DAOBox.list_boxes()
        id_boxes = [x[0] for x in boxes]
        planos = self.DAOPaciente.get_planos_de_saude(cpf)
        planos = [x.split(' - ')[0] for x in planos]
        planos = ['Sessão particular'] + planos


        layout  = [[sg.Text("Horario da sesão:"), sg.Combo(horarios,size=(10,1),
                                                             default_value = horarios[0],
                                                             readonly = True,
                                                             k='-TIME-')],
                   [sg.Text("Box:"), sg.Combo(id_boxes, size = (1,1),
                                              default_value = id_boxes[0],
                                              readonly = True,
                                              k = '-BOX-')],
                   [sg.Text("Plano de Saúde:"), sg.Combo(planos,
                                                         default_value = planos[0],
                                                         size = 60,
                                                         readonly = True,
                                                         k = '-PLANO-')],
                   [sg.Text("Data da Sessão",k = '-data-txt-')],
                   [sg.Input(k = '-data-', default_text = "dd/mm/aaaa")],
                   [sg.Text(k='err-data')],
                   [sg.Text("Observações")],
                   [sg.Input(k = '-obs-', size = (60, 30))],
                   [sg.Text(k='-W-', size = (60,1))],
                   [sg.Button("Ok", bind_return_key = True),
                   sg.Button("Cancelar")]
                   ]

        window = sg.Window('Cadastro Sessão', layout)

        while True:

            event, values = window.read()
            sessao = Entidades.Sessao()
            if event == "Cancelar" or event == sg.WIN_CLOSED :
                break

            if(event == 'Ok'):
                sessao.id_Horario = self.DAOHorario.get_id_horario( window['-TIME-'].get()[0] )

                is_okay = True
                try:
                    sessao.data_sessao = values['-data-']
                    sessao.id_DiaSemana  = sessao.data_sessao.weekday()+1
                except ValueError as err:
                    window['err-data'].update(err, text_color = 'red')
                    is_okay&=0
              
                sessao.idBox = values['-BOX-']
                sessao.observacoes = values['-obs-'] if values['-obs-'] else None
                sessao.Paciente_CPF = cpf;

                nome_plano = values['-PLANO-']


                if nome_plano == "Sessão particular":
                    sessao.id_PlanoDeSaude = None
                    sessao.particular = 1
                else :
                    sessao.id_PlanoDeSaude = self.DAOPaciente.get_id_plano(cpf, nome_plano)
                    sessao.particular = 0
                

                if is_okay:

                    try:
                        self.DAOSessao.insert(sessao)
                        break
                    except ValueError as err:
                        window['-W-'].update(err)
                    except Exception as err:
                        window['-W-'].update(err)

        window.close()

class Paciente:
    DAOPaciente = DAO.Paciente()
    DAOSessao = DAO.Sessao()
    APSessao = Sessao()

    def cadastro(self, cpf_existente = None):
        dados = {'data_nasc': 'dd/mm/aaaa'}
        if(cpf_existente):
            dados =  self.DAOPaciente.dados(cpf_existente)

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
                try:
                    if cpf_existente:
                        self.DAOPaciente.update(cpf_existente,paciente)
                    else:
                        self.DAOPaciente.insert(paciente)
                    break
                except ValueError as err:
                    window['err-cpf'].update(err, text_color='red')
                except Exception as err:
                    window['err-complemento'].update(err, text_color='red')

        window.close()
        return not cancelou

    def _lista_pacientes(self):
        lista = [(cpf, nome) for cpf, nome in
                 self.DAOPaciente.list()]
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
                        [sg.Text(k="-CPF-", size=(20, 1)),
                        sg.Text(k="-DATE-", size=(30, 1))],
                        [sg.Text(k="-CEP-", size=(20, 1)),
                        sg.Text(k="-COMP-", size=(30, 1))],
                        [sg.Text(k="-PLANO-", size=(60, 1))],
                        [sg.Listbox(k="-PLANOS-",
                                    values = [],
                                    visible = False,
                                    horizontal_scroll=True,
                                    size=(60, 3))],
                        [sg.Text(k="-C-TXT-", size=(60, 1))],
                        [sg.Listbox(k="-C-LIST-",
                                    values = [],
                                    visible = False,
                                    horizontal_scroll=True,
                                    size=(60, 4))],
                        [sg.Button("Consultar Sessão",
                                   k='-C-SE-',
                                   visible=False,
                                   disabled=True,
                                   )],
                        [sg.Button("Cadastrar Sessão",
                                   k='-ADD-SE-',
                                   visible=False,
                                   disabled=True,
                                   )],
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

            elif event == "-LIST-" and values["-LIST-"]:
                selecionado = values["-LIST-"][0].split(' - ')
                cpf = selecionado[0]
                paciente = self.DAOPaciente.dados(cpf)
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
                window['-PLANO-'].update('Códigos de cadastro em planos de saúde:')
                window['-PLANOS-'].update(self.DAOPaciente.get_planos_de_saude(cpf),
                                          visible = True)
                window['-DEL-'].update(disabled=False,
                                       visible=True)
                window['-UPD-'].update(disabled=False,
                                       visible=True)
                window['-C-TXT-'].update('Sessões:')
                window['-C-SE-'].update(disabled=False,
                                       visible=True)
                window['-ADD-SE-'].update(disabled=False,
                                       visible=True)
                window['-C-LIST-'].update(disabled=False,
                                          visible=True,
                                          values = self.DAOSessao.
                                          get_horario_sessoes_paciente(cpf))

            elif event == '-DEL-':


                freeze(window)
                if confirmar_acao():

                    self.DAOPaciente.delete(cpf)
                    window['-LIST-'].update(self._lista_pacientes(), disabled = False)
                    window['-TXT-'].update("Selecione um paciente")
                    window['-NOME-'].update('')
                    window['-CPF-'].update('')
                    window['-DATE-'].update('')
                    window['-CEP-'].update('')
                    window['-COMP-'].update('')
                    window['-PLANO-'].update('')
                    window['-DEL-'].update(visible = False)
                    window['-UPD-'].update(visible = False)
                    window['-C-TXT-'].update('')
                    window['-C-SE-'].update(visible = False)
                    window['-ADD-SE-'].update(visible = False)
                    window['-C-LIST-'].update(visible = False)
                    window['-PLANOS-'].update(visible = False)

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
                    window['-C-TXT-'].update('')
                    window['-PLANO-'].update('')
                    window['-COMP-'].update('')
                    window['-DEL-'].update(visible = False)
                    window['-UPD-'].update(visible = False)
                    window['-C-SE-'].update(visible = False)
                    window['-ADD-SE-'].update(visible = False)
                    window['-C-LIST-'].update(visible = False)
                    window['-PLANOS-'].update(visible = False)
                else:
                    unfreeze(window)
                
            elif event == '-C-SE-':
                res = window['-C-LIST-'].get()
                DAOHorario = DAO.Horario()
                if res :
                    keys = (res[0])
                    data = keys[0]
                    id_horario = DAOHorario.get_id_horario(keys[1])
                    freeze(window)
                    self.APSessao.display_sessao(cpf, data, id_horario)
                    unfreeze(window)
            elif event == '-ADD-SE-':
                freeze(window)
                self.APSessao.cadastro(cpf)
                unfreeze(window)
                window['-C-LIST-'].update(disabled=False,
                                          values = self.DAOSessao.
                                          get_horario_sessoes_paciente(cpf))




            

        window.close()


def menu_inicial():
    layout = [[sg.Text("Sistema Gerenciador de Clínicas", font = "Helvetica 26 bold")],
              [sg.Button("Pacientes", expand_x=True, k = '-PAC-'  )],
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

