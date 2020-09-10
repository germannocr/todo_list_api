import json
import os
import socket
from datetime import datetime
from decimal import Decimal
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from django.test import (
    TestCase,
    Client
)


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

client = Client()
API_URL = os.environ.get('API_URL', 'http://localhost:8000/')


def validate_emprestimo_saldo_devedor(saldo_devedor: float, taxa_juros: int, valor_pagamento: int):
    valor_juros = (saldo_devedor * taxa_juros) / 100

    valor_amortizacao = valor_pagamento - valor_juros

    saldo_devedor_resultante = saldo_devedor - valor_amortizacao

    return saldo_devedor_resultante


class EmprestimoCreation(TestCase):
    def setUp(self):
        user_payload = {
            "username": "germannocorreia",
            "password1": "senhadeteste",
            "password2": "senhadeteste"
        }
        response = client.post(
            f"{API_URL}registration/",
            data=json.dumps(user_payload),
            content_type='application/json'
        )

        self.token = json.loads(response.content)["token"]

        self.valid_payload = {
            "valor_nominal": 30000.00,
            "taxa_juros": 1.50,
            "banco": "Bradesco",
            "nome_cliente": "Matheus Cansian"
        }
        self.invalid_payload = {
            "valor_nominal": -30000.0,
            "taxa_juros": "1.50",
            "banco": 2,
            "nome_cliente": True
        }

    def test_create_emprestimo(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        response = client.post(
            f"{API_URL}createemprestimo/",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('valor_nominal'), '30000.00')
        self.assertEqual(response.get('saldo_devedor'), '30000.00')
        self.assertEqual(response.get('taxa_juros'), '1.50')
        self.assertEqual(response.get('banco'), self.valid_payload.get('banco'))
        self.assertEqual(response.get('nome_cliente'), self.valid_payload.get('nome_cliente'))
        self.assertEqual(response.get('data_solicitacao'), datetime.today().strftime("%Y-%m-%d"))
        self.assertEqual(response.get('endereco_ip'), ip_address)

        response = client.post(
            f"{API_URL}createemprestimo/",
            data=json.dumps(self.invalid_payload),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_emprestimo_get_list(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)

        response = client.post(
            f"{API_URL}createemprestimo/",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(
            f"{API_URL}getemprestimolist/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('valor_nominal'), '30000.00')
        self.assertEqual(response.get('saldo_devedor'), '30000.00')
        self.assertEqual(response.get('taxa_juros'), '1.50')
        self.assertEqual(response.get('banco'), self.valid_payload.get('banco'))
        self.assertEqual(response.get('nome_cliente'), self.valid_payload.get('nome_cliente'))
        self.assertEqual(response.get('data_solicitacao'), datetime.today().strftime("%Y-%m-%d"))
        self.assertEqual(response.get('endereco_ip'), ip_address)


class PagamentoCreation(TestCase):
    def setUp(self):
        user_payload = {
            "username": "germannocorreia",
            "password1": "senhadeteste",
            "password2": "senhadeteste"
        }
        response = client.post(
            f"{API_URL}registration/",
            data=json.dumps(user_payload),
            content_type='application/json'
        )

        self.token = json.loads(response.content)["token"]

        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        emprestimo_body = {
            "valor_nominal": 30000.00,
            "taxa_juros": 1.50,
            "banco": "Bradesco",
            "nome_cliente": "Matheus Cansian"
        }

        response = client.post(
            f"{API_URL}createemprestimo/",
            data=json.dumps(emprestimo_body),
            content_type='application/json',
            **headers
        )

        self.emprestimo_id = json.loads(response.content)["content"]["id"]

        self.valid_payload = {
            "identificador_emprestimo": self.emprestimo_id,
            "valor_pagamento": 2750.40,
        }

        self.invalid_payload = {
            "identificador_emprestimo": self.emprestimo_id,
            "valor_pagamento": False,
        }

    def test_create_pagamento_check_debit_balance(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        emprestimo_before_payment_response = client.get(
            f"{API_URL}getemprestimolist/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(emprestimo_before_payment_response.status_code, status.HTTP_200_OK)
        emprestimo_before_payment_response = json.loads(emprestimo_before_payment_response.content)["content"][0]

        saldo_devedor_before_payment = Decimal(emprestimo_before_payment_response.get('saldo_devedor'))

        response = client.post(
            f"{API_URL}createpagamento/",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('identificador_emprestimo'), self.valid_payload.get('identificador_emprestimo'))
        self.assertEqual(response.get('valor_pagamento'), '2750.40')

        emprestimo_response = client.get(
            f"{API_URL}getemprestimolist/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(emprestimo_response.status_code, status.HTTP_200_OK)
        emprestimo_response = json.loads(emprestimo_response.content)["content"][0]

        saldo_devedor_after_payment = Decimal(emprestimo_response.get('saldo_devedor'))

        retrieved_emprestimo_taxa_juros = Decimal(emprestimo_response.get('taxa_juros'))
        valor_pagamento = Decimal(response.get('valor_pagamento'))

        saldo_devedor_resultante = validate_emprestimo_saldo_devedor(
            saldo_devedor=saldo_devedor_before_payment,
            taxa_juros=retrieved_emprestimo_taxa_juros,
            valor_pagamento=valor_pagamento
        )

        self.assertEqual(saldo_devedor_after_payment, saldo_devedor_resultante)

    def test_create_pagamento_retrieve_pagamento_list(self):
        headers = {
            "HTTP_AUTHORIZATION": f"JWT {self.token}"
        }

        response = client.post(
            f"{API_URL}createpagamento/",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = client.get(
            f"{API_URL}getpagamentoslist/",
            content_type='application/json',
            **headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('identificador_emprestimo'), self.emprestimo_id)
        self.assertEqual(response.get('valor_pagamento'), '2750.40')
        self.assertEqual(response.get('data_pagamento'), datetime.today().strftime("%Y-%m-%d"))
