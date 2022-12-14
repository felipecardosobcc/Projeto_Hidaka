import sqlite3 as db
from tkinter import *
import flet as ft

def inicializar():
    banco = db.connect('questoes')
    cursor = banco.cursor()
    cursor.execute("""
CREATE TABLE questoes (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        comando TEXT NOT NULL,
        alternativas TEXT NOT NULL,
        reposta TEXT NOT NULL,
        tags TEXT
);
""")
    return banco


def inserir(banco, comando, alternativas, resposta, tags):
    cursor = banco.cursor()
    cursor.execute(f"""
    INSERT INTO questoes VALUES (NULL, '{comando}', '{alternativas}', '{resposta}', '{tags}')
    """)
    print(f"\nQuestão inserida.\n")
    banco.commit()


def excluir_questao(banco, id):
    cursor = banco.cursor()
    cursor.execute("""
DELETE FROM questoes
WHERE id = ?
""", (id,))
    print(f'Questão {id} excluída com sucesso.')


def visualizar_questoes(banco):
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM questoes")
    questoes = cursor.fetchall()
    return questoes


def questoes_tag(banco):
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM questoes")
    questoes = cursor.fetchall()
    tag = input('Digite a tag desejada: ')
    for element in questoes:
        print()
        if tag in element[4]:
            print(f'{element[0]}ª) {element[1]}\n{element[2]}\nResposta: alternativa {element[3]}\nTags associadas: {element[4]}')



def connect(banco):
    return db.connect(banco)


try:
    banco = inicializar()
except:
    banco = db.connect('questoes', check_same_thread=False)


janela = Tk() 
janela.title("Menu")
janela.geometry('250x250')

texto_auxiliar = Label(janela, text="Escolha uma das opções abaixo:\n")
texto_auxiliar.grid(column=0, row=0)

menu = Label(janela, text="1- Criar questão\n2- Excluir questão\n3- Pesquisar questões por tag\n4- Visualizar todas questões\n5- Sair\n")
menu.grid(column=0, row=1)

input = Entry(janela, width=5)
input.grid(column=0, row = 2)

def output():
    output = str(input.get())
    if output == '1':
        def main1(page:ft.Page):
            page.auto_scroll = True
            page.scroll = ft.ScrollMode.HIDDEN

            def Adicionar_Alternativa(e):
                Adicionar_Alternativa_btn.data+=1
                page.add(ft.Row([caixa_de_alternativa,Alternativa_Check_Verdadeira]))
                caixa_de_alternativa.label = F'Alternativa {chr(Adicionar_Alternativa_btn.data)}'
                alternativas.append(caixa_de_alternativa.value)
                caixa_de_alternativa.value = ''
                if Alternativa_Check_Verdadeira.value == True:
                    alternativa_correta.append(F'Alternativa {chr(Adicionar_Alternativa_btn.data-1)}')
                Alternativa_Check_Verdadeira.value=False
                page.update() 

            def Finalizar(e):
                alternativas.append(caixa_de_alternativa.value)
                if Alternativa_Check_Verdadeira.value == True:
                    alternativa_correta.append(F'Alternativa {chr(Adicionar_Alternativa_btn .data)}')
                page.dialog = Dialogo_Final
                Dialogo_Final.open = True
                page.update()

            def Salvar(e):
                dict_values['Comando'] = Enunciado.value
                dict_values['Alternativas'] = alternativas[1:]
                dict_values['Resposta'] = alternativa_correta
                dict_values['Tags'] = Caixa_Tags.value
                comando = dict_values['Comando']
                alternativas1 = dict_values['Alternativas']
                alternativas_tratadas = "\n".join(alternativas1)
                resposta = dict_values['Resposta']
                tags = dict_values['Tags']
                Dialogo_Final.open = False
                page.update()
                print(comando, alternativas_tratadas, resposta[0], tags)
                inserir(banco, comando, alternativas_tratadas, resposta[0], tags)

    
            alternativas = []
            alternativa_correta = []

    
            dict_values = {
                'Comando' : '',
                'Alternativas':'',
                'Resposta':'',
                'Tags':''
            }

            caixa_de_alternativa=ft.TextField(label=f'Alternativa)',bgcolor='cyan',autofocus=True,width=500)
            
            titulo = ft.Text(value="Gerenciador de questões",text_align='center')

            Enunciado = ft.TextField(label='1) Questão',bgcolor='blue200',autofocus=True, width=500)

            Adicionar_Alternativa_btn = ft.ElevatedButton('Adicionar Alternativa' ,icon='ADD', on_click=Adicionar_Alternativa,data=96)

            Caixa_Tags = ft.TextField(label='Tags', autofocus=True)

            Dialogo_Final = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Defina as Tags"),
                    content=ft.Text("Adicione Tags correspondente ao assunto da Questão"),
                    actions=[
                        Caixa_Tags,
                        ft.TextButton("Salvar", on_click=Salvar),
                    ]
                )

            Finalizar_btn = ft.ElevatedButton('Finalizar',icon=ft.icons.ARROW_FORWARD_ROUNDED,on_click=Finalizar)

            Alternativa_Check_Verdadeira = ft.Checkbox(label='Verdadeiro')

            page.add(
                ft.Column(
                    controls=[titulo,ft.Row([Enunciado,Adicionar_Alternativa_btn,Finalizar_btn])]
                )
            )
        ft.app(target=main1)

    elif output == '2':
        def main(page: ft.Page):

            page.auto_scroll = True

            def mostrar(e):
                a = visualizar_questoes(banco)
                for x in a:
                    ID = x[0]
                    comando = x[1]
                    alternativas = x[2]
                    resposta = x[3]
                    tag = x[4]
                    page.add(ft.Container(
                                content=ft.Text(f'Questão {ID})\nComando: {comando}\n Alternativas:\n{alternativas}\nresposta:{resposta}\nTags:{tag}\n'),
                                margin=10,
                                padding=10,
                                alignment=ft.alignment.center_left,
                                width=400,
                                height=200,
                                border_radius=10,
                                border=ft.border.all(5, ft.colors.BLUE_800)
                            )) 

            def excluir(e):
                excluir_questao(banco, Id.value)

            titulo = ft.Text(value="Excluir",text_align='center')   

            Mostrar = ft.ElevatedButton('Mostrar Questões' ,icon=ft.icons.SEARCH, on_click=mostrar) 

            Id = ft.TextField(label='Id',hint_text='Qual o número da questão que você deseja excluir?')

            btn_excluir = ft.ElevatedButton('Remover Questão',icon=ft.icons.HIGHLIGHT_REMOVE_OUTLINED,on_click=excluir)
            
            page.add(
                ft.Column(
                    [
                        titulo,
                        Mostrar,
                        ft.Row([Id,btn_excluir])
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
        ft.app(target=main)

    elif output == '3':
        def main(page:ft.Page):

            def mostrar(e):
                tag = Tag.value
                questoes = visualizar_questoes(banco)
                for questao in questoes :
                    if tag in questao[4]:
                        ID = questao[0]
                        comando = questao[1]
                        alternativas = questao[2]
                        resposta = questao[3]
                        tag = questao[4]
                        page.add(ft.Container(
                                content=ft.Text(f'Questão {ID})\nComando: {comando}\n Alternativas:\n{alternativas}\nresposta:{resposta}\nTags:{tag}\n'),
                                margin=10,
                                padding=10,
                                alignment=ft.alignment.center_left,
                                width=400,
                                height=200,
                                border_radius=10,
                                border=ft.border.all(5, ft.colors.BLUE_800)
                            ))
    
            titulo = ft.Text(value="Procurar questões",text_align='center')

            Tag = ft.TextField(label='TAG',hint_text='Digite a tag que você deseja procurar',bgcolor='blue200',autofocus=True, width=500,icon=ft.icons.SEARCH_ROUNDED)

            Final = ft.ElevatedButton('Finalizar',icon=ft.icons.ARROW_FORWARD_ROUNDED,on_click=mostrar)

            page.add(
                ft.Row(
                    [titulo],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Row(
                    [
                        ft.Container(
                            content=Tag,
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            width=700,
                            height=100,
                            border_radius=10,
                        ),
                        Final
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
        ft.app(target=main)
        
    elif output == '4':
        def main(page:ft.Page):
            page.auto_scroll = True

            def mostrar(e):
                a = visualizar_questoes(banco)
                for x in a:
                    ID = x[0]
                    comando = x[1]
                    alternativas = x[2]
                    resposta = x[3]
                    tag = x[4]
                    page.add(ft.Container(
                                content=ft.Text(f'Questão {ID})\nComando: {comando}\n Alternativas:\n{alternativas}\nresposta:{resposta}\nTags:{tag}\n'),
                                margin=10,
                                padding=10,
                                alignment=ft.alignment.center_left,
                                width=400,
                                height=200,
                                border_radius=10,
                                border=ft.border.all(5, ft.colors.BLUE_800)
                            )) 

            titulo = ft.ElevatedButton("Visualizar",on_click=mostrar)    
            
            page.add(
                ft.Row(
                    [
                        titulo,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )
        ft.app(target=main)
    elif output == '5':
        janela.destroy()
    else:
        erro = Label(janela, text="A entrada recebida é inválida,\ntente novamente.")
        erro.grid(column=0, row=4)


botao = Button(janela, text="Enter", command=output)
botao.grid(column=0, row=3)

janela.mainloop()

banco.close()