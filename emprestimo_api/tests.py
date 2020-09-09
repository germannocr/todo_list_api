import json
import os
import socket
from datetime import datetime

from django.test import TestCase, Client
from rest_framework import status

from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

client = Client()
API_URL = os.environ.get('API_URL', 'http://localhost:8000/')


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
            "valor_nominal": "30000.0",
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
