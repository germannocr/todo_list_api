from datetime import datetime

from django.contrib.auth.models import User

from emprestimo_api.models import Emprestimo, Pagamento


def retrieve_all_emprestimos(user_id: int):
    """
    Returns all objects of type Emprestimo

    #Parameters:
        user_id (int):User unique identifier

    #Returns:
        retrieved_emprestimo_list (list):List of Emprestimo objects created by the user who made the request
    """

    retrieved_emprestimo_list = Emprestimo.objects.filter(created_by_user=user_id).all()

    return retrieved_emprestimo_list


def retrieve_emprestimo(emprestimo_id: int, user_id: int):
    """
    Search for the Emprestimo object that has the given identifier

    #Parameters:
        emprestimo_id (int): Emprestimo object unique identifier
        user_id (int):User unique identifier

    #Returns:
        retrieved_emprestimo (Emprestimo):Emprestimo object created by the user who made the request
    """
    retrieved_emprestimo = Emprestimo.objects.filter(id=emprestimo_id, created_by_user=user_id).first()

    return retrieved_emprestimo


def retrieve_all_pagamentos(user_id: int):
    """
    Returns all objects of type Pagamento

    #Parameters:
        user_id (int):User unique identifier

    #Returns:
        retrieved_pagamentos_list (list):List of Pagamento objects created by the user who made the request
    """
    retrieved_pagamentos_list = Pagamento.objects.filter(created_by_user=user_id).all()

    return retrieved_pagamentos_list


def create_emprestimo(request_body: dict, request_user: User):
    """
    Creates a new object of type Emprestimo.

    #Parameters:
        request_body (dict):Body in JSON format with the necessary fields for creating a new Emprestimo.
        request_user (User):User type object that represents the user who made the request.

    #Returns:
        created_emprestimo (Emprestimo):New object of type Emprestimo created.
    """
    created_emprestimo = Emprestimo.objects.create(
        valor_nominal=request_body.get('valor_nominal'),
        taxa_juros=request_body.get('taxa_juros'),
        endereco_ip=request_body.get('endereco_ip'),
        data_solicitacao=datetime.today().strftime("%Y-%m-%d"),
        banco=request_body.get('banco'),
        nome_cliente=request_body.get('nome_cliente'),
        saldo_devedor=request_body.get('valor_nominal'),
        created_by_user=request_user.id
    )

    return created_emprestimo


def create_pagamento(request_body: dict, request_user: User):
    """
    Creates a new object of type Pagamento.

    #Parameters:
        request_body (dict):Body in JSON format with the necessary fields for creating a new Pagamento.
        request_user (User):User type object that represents the user who made the request.

    #Returns:
        created_pagamento(Pagamento):New object of type Pagamento created.
    """
    created_pagamento = Pagamento.objects.create(
        identificador_emprestimo=request_body.get('identificador_emprestimo'),
        valor_pagamento=request_body.get('valor_pagamento'),
        created_by_user=request_user.id,
        data_pagamento=datetime.today().strftime("%Y-%m-%d")
    )

    return created_pagamento
