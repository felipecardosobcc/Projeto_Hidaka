import banco_questoes as bq
from menu import main

while True:
    user = input('\nÉ sua primeira vez na plataforma? (y/n)\n')
    if user.lower() not in ['y', 'n']:
        print("Opção inválida, tente novamente.\n")
    elif user.lower() == 'y':
        banco = bq.inicializar()
        break
    else:
        banco = bq.connect('questoes')
        break

main(banco)

banco.close()