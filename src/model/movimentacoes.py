'''
model Transacoes()
'''
from datetime import datetime
from src.model.base_model import BaseModel
from src.util.data_e_hora_util import (
    converter_timestamp_to_datetime
)

class Movimentacoes(BaseModel):
    '''
    Dados da movimentação bancária de uma determinada conta do correntista.
    '''
    # pylint: disable=too-few-public-methods
    def __init__(
        # pylint: disable=too-many-arguments
        self,
        idt: int,
        valor: float,
        date: datetime,
        cliente_id: int,
        conta_id: int
    ) -> None:
        '''
        Inicialização da classe Transacoes
        '''
        super().__init__(idt)
        self.valor: float = valor
        self.date: datetime = date
        self.cliente_id:  int = cliente_id
        self.conta_id: int = conta_id

def movimentacao_from_dict(data: dict[str, str | datetime | float]) -> Movimentacoes:
    '''
    Recebe os dados e retorna Conta(id, numero, tipo, agencia_id, usuario_id e digito)
    '''
    data_informada = data.get('date')
    data_hora = converter_timestamp_to_datetime(data_informada) # type: ignore[arg-type]
    mov =  Movimentacoes(
        idt=data.get('id', 0),  # type: ignore[arg-type]
        valor=data.get('valor', 0),  # type: ignore[arg-type]
        date=data_hora,
        conta_id=data.get('conta_id', 0),  # type: ignore[arg-type]
        cliente_id=data.get('cliente_id', 0),  # type: ignore[arg-type]
    )
    return mov
