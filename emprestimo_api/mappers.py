import decimal
import socket
from decimal import Decimal

from django.http import JsonResponse
from rest_framework import status

from emprestimo_api.models import Emprestimo
from emprestimo_api.serializers import EmprestimoSerializer, PagamentoSerializer


def create_custom_fields(request_body: dict):
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    request_body['endereco_ip'] = ip_address

    return request_body


def map_post_emprestimo_response(serialized_response):
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_201_CREATED
    )


def map_post_pagamento_response(serialized_response):
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_201_CREATED
    )


def map_get_pagamento_response(serialized_response: PagamentoSerializer):
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def map_get_emprestimo_response(serialized_response: EmprestimoSerializer):
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def calculate_debit_balance(request_body: dict, retrieved_emprestimo: Emprestimo):

    taxa_juros = retrieved_emprestimo.taxa_juros
    saldo_devedor = Decimal(retrieved_emprestimo.saldo_devedor)

    valor_juros = (saldo_devedor * taxa_juros) / 100
    valor_pagamento = Decimal(request_body.get('valor_pagamento'))
    valor_amortizacao = valor_pagamento - valor_juros

    saldo_devedor_resultante = saldo_devedor - valor_amortizacao

    if saldo_devedor_resultante < 0:
        saldo_devedor_resultante = 0

    retrieved_emprestimo.saldo_devedor = saldo_devedor_resultante
    retrieved_emprestimo.save(force_update=True)

    return
