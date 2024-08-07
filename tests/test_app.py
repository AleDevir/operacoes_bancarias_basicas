# pylint: disable=line-too-long
'''
Testes do fluxo principal app.py
pytest tests/test_app.py -vv
'''

from unittest.mock import patch, call
from unittest import TestCase
from datetime import datetime

from src.app import (
    get_auth_na_conta,
    escolher_uma_opcao_do_menu_entrada,
    exibir_mensagem_de_boas_vindas,
    exibir_extrato,
    get_movimentacao_financeira_do_cliente,
    caixa_eletronico,
    sacar,
    depositar
)
from src.repositorio.carga_db_repositorio import carregar_banco_de_dados

def setup_module(module): # pylint: disable=unused-argument
    '''
    Setup na base de dados 
    '''
    carregar_banco_de_dados()



class Test(TestCase):
    '''
    Classe de teste para inputs.
    '''
    ################################################
     # TESTES USUÁRIO #
    ################################################

    @patch('src.app.input_int')
    @patch('src.app.get_senha')
    def test_obter_cliente_valido(self, get_senha, input_int):
        '''
        Teste para input das credenciais do usuario (conta e senha).  CONTA_E_SENHA-VÁLIDOS 
        python -m unittest -v tests.test_app.Test.test_obter_cliente_valido -v
        '''
        msg_conta = "\n Conta Corrente: "
        msg_senha = " Senha: "
        get_senha.return_value = '123'
        conta_usuario = 5555
        input_int.return_value = conta_usuario
        auth = get_auth_na_conta()
        self.assertIsNotNone(auth, 'Conta esperada não é CONTA')
        self.assertEqual(auth['conta_numero'], conta_usuario)
        input_int.assert_has_calls([
            call(msg_conta)
        ])
        get_senha.assert_has_calls([
            call(msg_senha)
        ])

    @patch('src.app.input_int')
    @patch('src.app.get_senha')
    def test_obter_cliente_senha_invalida(self, get_senha, input_int):
        '''
        Teste para input das credencial senha inválida do usuario (conta e senha).  SENHA-INVÁLIDA 
        python -m unittest -v tests.test_app.Test.test_obter_cliente_senha_invalida -v
        '''
        msg_conta = "\n Conta Corrente: "
        msg_senha = " Senha: "
        get_senha.side_effect = ['SENHA INVÁLIDA', '123']
        conta_usuario = 5555
        input_int.return_value = conta_usuario
        auth = get_auth_na_conta()
        self.assertIsNotNone(auth, 'Usuário esperado não é NONE')
        self.assertEqual(auth['conta_numero'], conta_usuario)
        input_int.assert_has_calls([
            call(msg_conta),
            call(msg_conta),
        ])
        get_senha.assert_has_calls([
            call(msg_senha),
            call(msg_senha),
        ])

        # error_message = f"Não foi possível obter a conta de número {conta_usuario}!"
        # with self.assertRaises(ValueError, msg=error_message):
        #             # Linha abaixo executa o método testado
        #             get_auth_na_conta()

    ########################################################
    # TESTES  ESCOLHER OPÇÃO DA OPERAÇÃO/E OU MOVIMENTÇÃO #
    #######################################################

    @patch('src.util.menu_util.input_opcoes')
    def test_escolher_uma_opcao_do_menu_entrada_valido(self, input_opcoes):
        '''
        Teste para input das opções do menu: ['E', D', 'S', 'F'] OPÇÃO-VÁLIDA.
        python -m unittest -v tests.test_app.Test.test_escolher_uma_opcao_do_menu_entrada_valido -v
        '''
        opcoes_do_menu_entrada = {
        'E': 'Extrato',
        'D': 'Depósito',
        'S': 'Saque', 
        'F': 'Finalizar e sair da conta.',
        }
        siglas: list[str] = list(opcoes_do_menu_entrada)
        msg = 'Entre com a opção desejada: '
        input_opcoes.return_value = 'E'
        opcao_escolhida = 'E'
        escolher_opcao = escolher_uma_opcao_do_menu_entrada(opcoes_do_menu_entrada)
        self.assertEqual(escolher_opcao, opcao_escolhida)
        input_opcoes.assert_has_calls([
            call(msg, siglas),
        ])

    @patch('src.util.menu_util.input_opcoes')
    def test_escolher_uma_opcao_do_menu_entrada_invalido(self, input_opcoes):
        '''
        Teste para input das opções do menu: ['E', D', 'S', 'F'] OPÇÃO-INVÁLIDA.
        python -m unittest -v tests.test_app.Test.test_escolher_uma_opcao_do_menu_entrada_invalido -v
        '''
        opcoes_do_menu_entrada = {
        'E': 'Extrato',
        'D': 'Depósito',
        'S': 'Saque', 
        'F': 'Finalizar e sair da conta.',
        }
        siglas: list[str] = list(opcoes_do_menu_entrada)
        msg = 'Entre com a opção desejada: '
        opcao_escolhida = 'E'
        input_opcoes.side_effect = ['OPÇÃO INVÁLIDA', opcao_escolhida]
        escolher_opcao = escolher_uma_opcao_do_menu_entrada(opcoes_do_menu_entrada)
        self.assertEqual(escolher_opcao, opcao_escolhida)
        input_opcoes.assert_has_calls([
            call(msg, siglas),
            call(msg, siglas),
        ])

    ##################################################
     # TESTES OPERAÇÕES SACAR / DEPOSITAR #
    ##################################################

    @patch('src.app.input_float')
    def test_sacar_valido(self, input_float):
        '''
        Teste do metodo sacar() - OPÇÃO VÁLIDA
        python -m unittest -v tests.test_app.Test.test_sacar_valido -v
        '''
        conta_id = 1

        msg = "Entre com o valor do saque R$: "
        saque = 50
        input_float.return_value = saque
        sacar(conta_id)
        input_float.assert_has_calls([
            call(msg)
        ])

    @patch('src.app.input_float')
    def test_sacar_valor_invalido(self, input_float):
        '''
        Teste do metodo sacar() - OPÇÃO INVÁLIDA
        python -m unittest -v tests.test_app.Test.test_sacar_valor_invalido -v
        '''
        conta_id = 2

        msg = "Entre com o valor do saque R$: "
        saque = 10
        input_float.side_effect = [-1, saque]
        sacar(conta_id)
        input_float.assert_has_calls([
            call(msg),
            call(msg),
        ])

    def test_sacar_excedeu_o_limite_do_dia(self):
        '''
        Teste do metodo sacar() - OPÇÃO INVÁLIDA
        python -m unittest -v tests.test_app.Test.test_sacar_excedeu_o_limite_do_dia -v
        '''
        conta_id = 4

        sacar(conta_id)
        assert True # Você já atingiu o limite de saques por dia!

    @patch('src.app.input_float')
    def test_depositar_valido(self, input_float):
        '''
        Teste do metodo depositar() - OPÇÃO VÁLIDA
        python -m unittest -v tests.test_app.Test.test_depositar_valido -v
        '''
        conta_id = 2

        msg = "\nEntre com o valor do depósito R$: "
        deposito = 50
        input_float.return_value = deposito
        depositar(conta_id)
        input_float.assert_has_calls([
            call(msg)
        ])

    @patch('src.app.input_float')
    def test_depositar_invalido(self, input_float):
        '''
        Teste do metodo depositar() - OPÇÃO INVÁLIDA
        python -m unittest -v tests.test_app.Test.test_depositar_invalido -v
        '''
        conta_id = 2

        msg = "\nEntre com o valor do depósito R$: "
        deposito = 50
        input_float.side_effect = [-1, deposito]
        depositar(conta_id)
        input_float.assert_has_calls([
            call(msg)
        ])


    ################################################
     # TESTES DO FLUXO PRINCIPAL -> app #
    ################################################
    @patch('src.app.exibir_extrato')
    @patch('src.app.depositar')
    @patch('src.app.sacar')
    @patch('src.app.escolher_uma_opcao_do_menu_entrada')
    # @patch('src.app..exibir_mensagem_de_boas_vindas')
    @patch('src.app.get_auth_na_conta')
    def test_caixa_eletronico_opcao( # pylint: disable=too-many-arguments
        self,
        get_auth_na_conta_mock,
        escolher_uma_opcao_do_menu_entrada_mock,
        sacar_mock,
        depositar_mock,
        exibir_extrato_mock,
    ):
        '''
        Teste do fluxo principal - caixa_eletronico() 
        python -m unittest -v tests.test_app.Test.test_caixa_eletronico_opcao -v
        '''
        get_auth_na_conta_mock.return_value =  {
            'conta_id': 5,
            'cliente_nome': 'test'
        }
        escolher_uma_opcao_do_menu_entrada_mock.side_effect = ['D', 'E', 'S', 'F']
        exibir_extrato_mock.return_value = None
        depositar_mock.return_value = None
        sacar_mock.return_value = None
        caixa_eletronico()

###############################################
    # TESTES SAUDAÇÃO USUÁRIO #
###############################################

def test_mensagem_boas_vindas_bom_dia():
    '''
    Teste para mensagem de boas vindas com bom dia.
    pytest tests/test_app.py::test_mensagem_boas_vindas_bom_dia -vv
    '''
    nome_usuario = 'test'
    hora_manha= datetime(2021, 6, 10, 6, 10, 00)
    exibir_mensagem_de_boas_vindas(nome_usuario, hora_manha)
    assert True

def test_mensagem_boas_vindas_boa_tarde():
    '''
    Teste para mensagem de boas vindas com boa tarde.
    pytest tests/test_app.py::test_mensagem_boas_vindas_boa_tarde -vv
    '''
    nome_usuario = 'test'
    hora_tarde= datetime(2021, 6, 10, 16, 10, 00)
    exibir_mensagem_de_boas_vindas(nome_usuario, hora_tarde)
    assert True

def test_mensagem_boas_vindas_boa_noite():
    '''
    Teste para mensagem de boas vindas com boa noite.
    pytest tests/test_app.py::test_mensagem_boas_vindas_boa_noite -vv
    '''
    nome_usuario = 'test'
    hora_noite= datetime(2021, 6, 10, 22, 10, 00)
    exibir_mensagem_de_boas_vindas(nome_usuario, hora_noite)
    assert True

###########################################################
    # TESTES  DAS MOVIMENTAÇÕES #
##########################################################
def test_get_movimentacao_financeira_do_cliente_valida():
    '''
    Teste do metodo get_movimentacao_financeira_do_usuario - VÁLIDO
    pytest tests/test_app.py::test_get_movimentacao_financeira_do_cliente_valida -vv
    '''
    conta_id = 1
    movimentacoes = get_movimentacao_financeira_do_cliente(conta_id)
    for movimentacao in movimentacoes:
        assert movimentacao.conta_id == conta_id

def test_get_movimentacao_financeira_do_cliente_invalida():
    '''
    Teste do metodo get_movimentacao_financeira_do_usuario - INVÁLIDO
    pytest tests/test_app.py::test_get_movimentacao_financeira_do_cliente_invalida -vv
    '''
    cliente_id = 999
    movimentacoes = get_movimentacao_financeira_do_cliente(cliente_id)
    for movimentacao in movimentacoes:
        assert movimentacao.cliente_id == cliente_id

def test_exibir_extrato():
    '''
    Teste do metodo exibir_extrato 
    pytest tests/test_app.py::test_exibir_extrato -vv
    '''
    cliente_id = 5
    exibir_extrato(cliente_id)
    assert True
