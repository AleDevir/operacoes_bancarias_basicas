'''
Aplicação do administrador.
    Carregar o DB.
    RUD no DB - Sqlite
'''

import bcrypt
from src.util.console_util import (
    bright_amarelo,
    print_center,
    limpar_console
)
from src.util.menu_util import escolher_uma_opcao_do_menu_entrada
from src.util.input_util import  input_int
from src.app import get_input, get_senha
from src.repositorio.carga_db_repositorio import carregar_banco_de_dados
from src.repositorio.cliente_repositorio import inserir_cliente
from src.repositorio.conta_repositorio import inserir_conta
from src.repositorio.agencia_repositorio import inserir_agencia
from src.util.console_util import verde

##################################################
     # OPÇOES DO MENU ADMIN#
##################################################
menu_admin:  dict[str, str ] = {
        'CB': 'Carregar a Base de Dados',
        'CL': 'Cliente',
        'CO': 'Conta',
        'AG': 'Agência', 
        'SA': 'Sair',
}
menu_crud:  dict[str, str ] = {
        'A': 'Adicionar',
        'D': 'Deletar',
        'U': 'Update', 
        'S': 'Sair',
}


##################################################
     # FLUXO PRINCIPAL DA APP_ADMIN #
##################################################

def admin() -> None:
    '''
    Fluxo Principal do Administrador.
    '''
    limpar_console()

    while True:
        opcao_administrativa = escolher_uma_opcao_do_menu_entrada(menu_admin)
        match opcao_administrativa:
            case "C":
                carregar_banco_de_dados()
                print(verde('Carregada com sucesso! :)'))
                break
            case "CL":
                opcao_crud = escolher_uma_opcao_do_menu_entrada(menu_crud)
                match opcao_crud:
                    case "A":
                        nome = get_input('Nome: ')
                        sobrenome = get_input('Sobrenome: ')
                        senha = get_senha('Senha: ')
                        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
                        cpf = get_input('CPF: ')
                        inserir_cliente(nome, sobrenome, senha_hash, cpf)
                    case "D":
                        print('DELETAR')
                    case "U":
                        print('UPADATE')
                    case "S":
                        print_center(bright_amarelo(" SAIR :)\n"), 40)
                        break
            case "CO":
                opcao_crud = escolher_uma_opcao_do_menu_entrada(menu_crud)
                match opcao_crud:
                    case "A":
                        numero = input_int('Numero da conta: ')
                        digito = input_int('Digito: ')
                        tipo = input_int('Tipo (1: conta-corrente | 2: poupança): ')
                        agencia_id = input_int('Agencia_id: ')
                        cliente_id = input_int('Cliente_id: ')
                        inserir_conta(numero, digito, tipo, agencia_id, cliente_id)
                    case "D":
                        print('DELETAR')
                    case "U":
                        print('UPADATE')
                    case "S":
                        print_center(bright_amarelo(" SAIR :)\n"), 40)
                        break
            case "AG":
                opcao_crud = escolher_uma_opcao_do_menu_entrada(menu_crud)
                match opcao_crud:
                    case "A":
                        numero = input_int('Numero da agência: ')
                        digito = input_int('Digito: ')
                        inserir_agencia(numero, digito)
                    case "D":
                        print('DELETAR')
                    case "U":
                        print('UPADATE')
                    case "S":
                        print_center(bright_amarelo(" SAIR :)\n"), 40)
                        break
            case "SA":
                print_center(bright_amarelo(" SAIR :)\n"), 40)
                break
    