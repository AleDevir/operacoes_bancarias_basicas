'''
model Transacoes()
'''
from datetime import datetime
from src.model.base_model import BaseModel

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
        usuario_id: int,
        conta_id: int
    ) -> None:
        '''
        Inicialização da classe Transacoes
        '''
        super().__init__(idt)
        self.valor: float = valor
        self.date: datetime = date
        self.usuario_id:  int = usuario_id
        self.conta_id: int = conta_id

def movimentacao_from_dict(data: dict[str, str | datetime | float]) -> Movimentacoes:
    '''
    Recebe os dados e retorna Conta(id, numero, tipo, agencia_id, usuario_id e digito)
    '''
    return Movimentacoes(
        idt=data.get('id', 0),  # type: ignore[arg-type]
        valor=data.get('valor', 0),  # type: ignore[arg-type]
        date=data.get('date', datetime(1900, 1, 1, 00, 00, 00)),  # type: ignore[arg-type]
        conta_id=data.get('conta_id', 0),  # type: ignore[arg-type]
        usuario_id=data.get('usuario_id', 0),  # type: ignore[arg-type]
    )
