import banco_questoes as bq

def menu(banco):
    while True:
        print()
        print("Menu de operações:")
        print("1- Criar questão\n2- Excluir questão\n3- Pesquisar questões por tag\n4- Visualizar todas questões\n5- Sair")
        option = int(input('Digite sua escolha: '))
        if option == 1:
            bq.criar_questao(banco)
        elif option == 2:
            bq.excluir(banco)
        elif option == 3:
            bq.questoes_tag(banco)
        elif option == 4:
            bq.visualizar_questoes(banco)
        elif option == 5:
            print("Operação finalizada.\n")
            break
        else:
            print("Erro: a opção inserida é inválida, tente novamente.")


def main(banco):
    return menu(banco)