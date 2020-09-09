from decimal import Decimal

from emprestimo_api.exceptions import MissingRequiredFields, InvalidFieldType, InvalidFieldValue, EmprestimoAlreadyPaid
from emprestimo_api.models import Emprestimo


def validate_emprestimo_identifier(emprestimo_id: int):
    if not isinstance(emprestimo_id, int):
        raise InvalidFieldType(code=400)

    if emprestimo_id <= 0:
        raise InvalidFieldValue(code=400)


def validate_emprestimo_post_body(request_body: dict):
    required_fields = [
        'valor_nominal',
        'taxa_juros',
        'banco',
        'nome_cliente'
    ]
    request_fields = request_body.keys()

    for current_required_field in required_fields:
        if current_required_field not in request_fields:
            raise MissingRequiredFields(code=400)

        if not isinstance(request_body.get('taxa_juros'), float):
            raise InvalidFieldType(code=400)


def validate_pagamento_post_body(request_body: dict):
    required_fields = [
        'identificador_emprestimo',
        'valor_pagamento'
    ]
    request_fields = request_body.keys()

    for current_required_field in required_fields:
        if current_required_field not in request_fields:
            raise MissingRequiredFields(code=400)


def validate_saldo_devedor(retrieved_emprestimo: Emprestimo):
    saldo_devedor = Decimal(retrieved_emprestimo.saldo_devedor)

    if saldo_devedor <= 0:
        raise EmprestimoAlreadyPaid(code=400)
