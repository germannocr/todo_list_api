from decimal import Decimal
from emprestimo_api.models import Emprestimo
from emprestimo_api.exceptions import (
    MissingRequiredFields,
    InvalidFieldType,
    InvalidFieldValue,
    EmprestimoAlreadyPaid
)


def validate_emprestimo_identifier(emprestimo_id: int):
    """
    Validates the unique ID of an Emprestimo, with respect to type and value.

    #Parameters:
        emprestimo_id (int): Unique identifier of an Emprestimo

    #Returns:
    """
    if not isinstance(emprestimo_id, int):
        raise InvalidFieldType(code=400)

    if emprestimo_id <= 0:
        raise InvalidFieldValue(code=400)

    return


def validate_emprestimo_post_body(request_body: dict):
    """
    Validates the JSON dictionary sent by the user when creating an Emprestimo.

    #Parameters:
        request_body (dict): Dictionary in JSON format sent by the user with the fields to create an Emprestimo.

    #Returns:
    """
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

    if not isinstance(request_body.get('valor_nominal'), float):
        raise InvalidFieldType(code=400)

    if not isinstance(request_body.get('banco'), str):
        raise InvalidFieldType(code=400)

    if not isinstance(request_body.get('nome_cliente'), str):
        raise InvalidFieldType(code=400)

    if request_body.get('valor_nominal') <= 0 or request_body.get('taxa_juros') <= 0:
        raise InvalidFieldValue(code=400)

    return


def validate_pagamento_post_body(request_body: dict):
    """
    Validates the JSON dictionary sent by the user when creating a Pagamento.

    #Parameters:
        request_body (dict): Dictionary in JSON format sent by the user with the fields to create a Pagamento.

    #Returns:
    """
    required_fields = [
        'identificador_emprestimo',
        'valor_pagamento'
    ]
    request_fields = request_body.keys()

    for current_required_field in required_fields:
        if current_required_field not in request_fields:
            raise MissingRequiredFields(code=400)

    if not isinstance(request_body.get('identificador_emprestimo'), int):
        raise InvalidFieldType(code=400)

    if request_body.get('identificador_emprestimo') <= 0:
        raise InvalidFieldValue(code=400)

    if not isinstance(request_body.get('valor_pagamento'), float):
        raise InvalidFieldType(code=400)

    if request_body.get('valor_pagamento') <= 0:
        raise InvalidFieldValue(code=400)

    return


def validate_saldo_devedor(retrieved_emprestimo: Emprestimo):
    """
    Validates that the debit balance of a given Emprestimo has a valid amount.

    #Parameters:
        retrieved_emprestimo (Emprestimo): Emprestimo type object that will have its debit balance validated.

    #Returns:
    """
    saldo_devedor = Decimal(retrieved_emprestimo.saldo_devedor)

    if saldo_devedor <= 0:
        raise EmprestimoAlreadyPaid(code=400)

    return
