import sqlite3 as db

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


def excluir(banco):
    cursor = banco.cursor()
    id = int(input('Qual o número da questão que você deseja excluir?\n'))
    cursor.execute("""
DELETE FROM questoes
WHERE id = ?
""", (id,))
    print(f'Questão {id} excluída com sucesso.')


def visualizar_questoes(banco):
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM questoes")
    questoes = cursor.fetchall()
    for element in questoes:
        print()
        print(f'{element[0]}ª) {element[1]}\n{element[2]}\nResposta: alternativa {element[3]}\nTags associadas: {element[4]}\n')


def questoes_tag(banco):
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM questoes")
    questoes = cursor.fetchall()
    tag = input('Digite a tag desejada: ')
    for element in questoes:
        print()
        if tag in element[4]:
            print(f'{element[0]}ª) {element[1]}\n{element[2]}\nResposta: alternativa {element[3]}\nTags associadas: {element[4]}')


def criar_alternativas():
    lista = []
    while True:
        lista.append(input('Escreva sua alternativa:\n'))
        controle = input('Deseja adicionar mais uma alternativa? (y/n)\n')
        if controle.lower() not in ['y', 'n']:
            print("Opção inválida, tente novamente.")
        elif controle == 'y':
            continue
        else:
            alternativas_tratadas = "\n".join(lista)
            return alternativas_tratadas


def criar_questao(banco):
    lista_tags = []
    comando = input('Insira o comando da questão:\n')
    alternativas = criar_alternativas()
    resposta = (input('Insira a resposta da questão:\n'))
    while True:
        controle = input('Gostaria de adicionar alguma tag à sua questão? (y/n)\n')
        if controle.lower() not in ['y', 'n']:
            print("Erro: opção inválida, tente novamente.")
        elif controle.lower() == 'y':
            tag = input('Digite a tag: ')
            lista_tags.append(tag)
        else:
            if len(lista_tags) > 0:
                tags_tratadas = " ".join(lista_tags)
                inserir(banco, comando, alternativas, resposta, tags_tratadas)
            else:
                null = "NULL"
                inserir(banco, comando, alternativas, resposta, null)
            break


def connect(banco):
    return db.connect(banco)