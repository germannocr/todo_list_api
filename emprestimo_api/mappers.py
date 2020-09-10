import socket
from decimal import Decimal

from rest_framework.serializers import ModelSerializer

from emprestimo_api.models import Emprestimo
from django.http import JsonResponse
from rest_framework import status
from emprestimo_api.exceptions import EmprestimoPaidAmountExceeded
from emprestimo_api.serializers import (
    EmprestimoSerializer,
    PagamentoSerializer
)


def create_custom_fields(request_body: dict):
    """
    Creates a new field that stores the IP address of the user who made the request.

    #Parameters:
        request-body (dict): Dictionary in JSON format passed by the user in the request.

    #Returns:
        request-body (dict): Dictionary in JSON format modified with new field added.
    """
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    request_body['endereco_ip'] = ip_address

    return request_body


def map_post_emprestimo_response(serialized_response: ModelSerializer):
    """
    Returns a response in JSON format with the fields present in the Emprestimo model.

    #Parameters:
        serialized_response (ModelSerializer): Serializer created from the Emprestimo model

    #Returns:
        (JsonResponse): Dictionary in JSON format with the data of a created object of type Emprestimo.
    """
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_201_CREATED
    )


def map_post_pagamento_response(serialized_response):
    """
    Returns a response in JSON format with the fields present in the Pagamento model.

    #Parameters:
        serialized_response (ModelSerializer): Serializer created from the Pagamento model

    #Returns:
        (JsonResponse): Dictionary in JSON format with the data of a created object of type Pagamento.
    """
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_201_CREATED
    )


def map_get_pagamento_response(serialized_response: PagamentoSerializer):
    """
    Returns a response in JSON format with the fields present in the Pagamento model.

    #Parameters:
        serialized_response (ModelSerializer): Serializer created from the Pagamento model

    #Returns:
        (JsonResponse): Dictionary in JSON format with the data of a retrieved object of type Pagamento.
    """
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def map_get_emprestimo_response(serialized_response: EmprestimoSerializer):
    """
    Returns a response in JSON format with the fields present in the Emprestimo model.

    #Parameters:
        serialized_response (ModelSerializer): Serializer created from the Emprestimo model

    #Returns:
        (JsonResponse): Dictionary in JSON format with the data of a retrieved object of type Emprestimo.
    """
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def update_debit_balance(request_body: dict, retrieved_emprestimo: Emprestimo):
    """
    Debits the outstanding balance of a given Emprestimo the amount of a payment that has been made on that Emprestimo.

    #Parameters:
        request_body (dict): Dictionary with the data passed by the user when creating a Pagamento.
        retrieved_emprestimo (Emprestimo): Emprestimo related to the created Pagamento.

    #Returns:
    """

    taxa_juros = retrieved_emprestimo.taxa_juros
    saldo_devedor = Decimal(retrieved_emprestimo.saldo_devedor)

    valor_juros = (saldo_devedor * taxa_juros) / 100
    valor_pagamento = Decimal(request_body.get('valor_pagamento'))
    valor_amortizacao = valor_pagamento - valor_juros

    saldo_devedor_resultante = saldo_devedor - valor_amortizacao

    if saldo_devedor_resultante < 0:
        raise EmprestimoPaidAmountExceeded(code=400)

    retrieved_emprestimo.saldo_devedor = saldo_devedor_resultante
    retrieved_emprestimo.save(force_update=True)

    return
