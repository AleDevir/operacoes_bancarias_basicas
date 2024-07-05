'''
Data e hora 
'''
from datetime import datetime

def converter_em_data_e_hora(data_str: str, formatacao: str = '%Y-%m-%d %H:%M:%S') -> datetime:
    '''
    Converte o TEXTO em data e hora ex: 29/06/2024 09:26
    '''
    date = datetime.strptime(data_str, formatacao)
    return date


def formatar_data_e_hora(data_hora: datetime = datetime.now()) -> str:
    '''
    Formata a data e hora ex: 29/06/2024 09:26
    '''
    data_e_hora_atuais_em_texto: str = data_hora.strftime('%d/%m/%Y %H:%M')
    return data_e_hora_atuais_em_texto

def exibir_data_e_hora() -> None:
    '''
    Exibe no console a data e hora atual ex: 29/06/2024 09:26
    '''
    print(f"Em: {formatar_data_e_hora()}")
