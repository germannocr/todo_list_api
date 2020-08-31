import json
import os

from django.test import TestCase, Client
from rest_framework import status

from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

client = Client()
API_URL = os.environ.get('API_URL', 'http://localhost:8000/')

# Create your tests here.
from navedexapi.models import Naver, Project


class NaverTest(TestCase):

    def setUp(self):
        user = User.objects.first()
        payload = jwt_payload_handler(user)
        self.token = jwt_encode_handler(payload)

        Naver.objects.create(
            id=1,
            name="Germanno Correia",
            birthdate="18-08-1996",
            admission_date="31-08-2020",
            job_role="Backend Developer",
            projects=[1],
            created_by_user=1
        )

        self.valid_payload = {
            "name": "João Pedro",
            "birthdate": "01-01-1996",
            "admission_date": "18-08-2020",
            "job_role": "CTO",
            "projects": [1]
        }

        self.invalid_payload = {
            "name": 2,
            "birthdate": "01-01-1996",
            "admission_date": "18-08-2020",
            "job_role": True,
            "projects": "[1]"
        }

    def test_create_naver(self):
        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.post(
            f"{API_URL}createnaver",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('name'), 'João Pedro')
        self.assertEqual(response.get('birthdate'), '01-01-1996')
        self.assertEqual(response.get('admission_date'), '18-08-2020')
        self.assertEqual(response.get('job_role'), 'CTO')
        self.assertEqual(response.get('projects'), [1])

        response = client.post(
            f"{API_URL}createnaver",
            data=json.dumps(self.invalid_payload),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_naver_get_by_id(self):
        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.post(
            f"{API_URL}createnaver",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('name'), 'João Pedro')
        self.assertEqual(response.get('birthdate'), '01-01-1996')
        self.assertEqual(response.get('admission_date'), '18-08-2020')
        self.assertEqual(response.get('job_role'), 'CTO')
        self.assertEqual(response.get('projects'), [1])

        naver_id = response.get('id')

        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.get(
            f"{API_URL}getnaver/{naver_id}",
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('name'), 'João Pedro')
        self.assertEqual(response.get('birthdate'), '01-01-1996')
        self.assertEqual(response.get('admission_date'), '18-08-2020')
        self.assertEqual(response.get('job_role'), 'CTO')
        self.assertEqual(response.get('projects'), [1])

    def test_create_naver_get_list(self):
        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.post(
            f"{API_URL}createnaver",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('name'), 'João Pedro')
        self.assertEqual(response.get('birthdate'), '01-01-1996')
        self.assertEqual(response.get('admission_date'), '18-08-2020')
        self.assertEqual(response.get('job_role'), 'CTO')
        self.assertEqual(response.get('projects'), [1])

        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.get(
            f"{API_URL}getnaverslist/",
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'João Pedro')
        self.assertEqual(response.get('birthdate'), '01-01-1996')
        self.assertEqual(response.get('admission_date'), '18-08-2020')
        self.assertEqual(response.get('job_role'), 'CTO')
        self.assertEqual(response.get('projects'), [1])

    def test_create_naver_update(self):
        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.post(
            f"{API_URL}createnaver",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('name'), 'João Pedro')
        self.assertEqual(response.get('birthdate'), '01-01-1996')
        self.assertEqual(response.get('admission_date'), '18-08-2020')
        self.assertEqual(response.get('job_role'), 'CTO')
        self.assertEqual(response.get('projects'), [1])

        naver_id = response.get('id')

        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.get(
            f"{API_URL}getnaver/{naver_id}",
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'João Pedro')
        self.assertEqual(response.get('birthdate'), '01-01-1996')
        self.assertEqual(response.get('admission_date'), '18-08-2020')
        self.assertEqual(response.get('job_role'), 'CTO')
        self.assertEqual(response.get('projects'), [1])

        patch_body = {
            "name": "Teste",
            "birthdate": "01-11-1996",
            "admission_date": "31-04-2020",
            "job_role": "Frontend Dev",
            "projects": [1]
        }

        headers = {
            "Authorization": f"JWT {self.token}"
        }

        response = client.patch(
            f"{API_URL}updatenaver/{naver_id}",
            data=json.dumps(patch_body),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'Teste')
        self.assertEqual(response.get('birthdate'), '01-11-1996')
        self.assertEqual(response.get('admission_date'), '31-04-2020')
        self.assertEqual(response.get('job_role'), 'Frontend Dev')
        self.assertEqual(response.get('projects'), [1])

        headers = {
            "Authorization": f"JWT {self.token}"
        }

        response = client.get(
            f"{API_URL}getnaver/{naver_id}",
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'Teste')
        self.assertEqual(response.get('birthdate'), '01-11-1996')
        self.assertEqual(response.get('admission_date'), '31-04-2020')
        self.assertEqual(response.get('job_role'), 'Frontend Dev')
        self.assertEqual(response.get('projects'), [1])

    def test_create_naver_delete(self):
        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.post(
            f"{API_URL}createnaver",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('name'), 'João Pedro')
        self.assertEqual(response.get('birthdate'), '01-01-1996')
        self.assertEqual(response.get('admission_date'), '18-08-2020')
        self.assertEqual(response.get('job_role'), 'CTO')
        self.assertEqual(response.get('projects'), [1])

        naver_id = response.get('id')

        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.get(
            f"{API_URL}getnaver/{naver_id}",
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'João Pedro')
        self.assertEqual(response.get('birthdate'), '01-01-1996')
        self.assertEqual(response.get('admission_date'), '18-08-2020')
        self.assertEqual(response.get('job_role'), 'CTO')
        self.assertEqual(response.get('projects'), [1])

        headers = {
            "Authorization": f"JWT {self.token}"
        }

        client.delete(
            f"{API_URL}deletenaver/{naver_id}",
            content_type='application/json',
            headers=headers
        )

        headers = {
            "Authorization": f"JWT {self.token}"
        }

        response = client.get(
            f"{API_URL}getnaver/{naver_id}",
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ProjectTest(TestCase):

    def setUp(self):
        user = User.objects.first()
        payload = jwt_payload_handler(user)
        self.token = jwt_encode_handler(payload)

        Project.objects.create(
            id=1,
            name="Navedex",
            navers=[1],
            created_by_user=1
        )

        self.valid_payload = {
            "name": "Navedex GUI",
            "navers": [1]
        }

        self.invalid_payload = {
            "name": ["Navedex website"],
            "navers": '[1]'
        }

    def test_create_project(self):
        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.post(
            f"{API_URL}createproject",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('name'), 'Navedex GUI')
        self.assertEqual(response.get('navers'), [1])

        response = client.post(
            f"{API_URL}createproject",
            data=json.dumps(self.invalid_payload),
            content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_project_get_by_id(self):
        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.post(
            f"{API_URL}createproject",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('name'), 'Navedex GUI')
        self.assertEqual(response.get('navers'), [1])

        project_id = response.get('id')

        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.get(
            f"{API_URL}getproject/{project_id}",
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('name'), 'Navedex GUI')
        self.assertEqual(response.get('navers'), [1])

    def test_create_project_get_list(self):
        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.post(
            f"{API_URL}createproject",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('name'), 'Navedex GUI')
        self.assertEqual(response.get('navers'), [1])

        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.get(
            f"{API_URL}getprojectlist/",
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'Navedex GUI')
        self.assertEqual(response.get('navers'), [1])

    def test_create_project_update(self):
        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.post(
            f"{API_URL}createproject",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('name'), 'Navedex GUI')
        self.assertEqual(response.get('navers'), [1])

        project_id = response.get('id')

        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.get(
            f"{API_URL}getproject/{project_id}",
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'Navedex GUI')
        self.assertEqual(response.get('navers'), [1])

        patch_body = {
            "name": "Projeto de teste",
            "navers": [2]
        }

        headers = {
            "Authorization": f"JWT {self.token}"
        }

        response = client.patch(
            f"{API_URL}updateproject/{project_id}",
            data=json.dumps(patch_body),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'Projeto de Teste')
        self.assertEqual(response.get('navers'), [1])

        headers = {
            "Authorization": f"JWT {self.token}"
        }

        response = client.get(
            f"{API_URL}getproject/{project_id}",
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'Projeto de teste')
        self.assertEqual(response.get('navers'), [1])

    def test_create_project_delete(self):
        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.post(
            f"{API_URL}createproject",
            data=json.dumps(self.valid_payload),
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = json.loads(response.content)["content"]
        self.assertEqual(response.get('name'), 'Navedex GUI')
        self.assertEqual(response.get('navers'), [1])

        project_id = response.get('id')

        headers = {
            "Authorization": f"JWT {self.token}"
        }
        response = client.get(
            f"{API_URL}getproject/{project_id}",
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = json.loads(response.content)["content"][0]
        self.assertEqual(response.get('name'), 'Navedex GUI')
        self.assertEqual(response.get('navers'), [1])

        headers = {
            "Authorization": f"JWT {self.token}"
        }

        client.delete(
            f"{API_URL}deleteproject/{project_id}",
            content_type='application/json',
            headers=headers
        )

        headers = {
            "Authorization": f"JWT {self.token}"
        }

        response = client.get(
            f"{API_URL}getproject/{project_id}",
            content_type='application/json',
            headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
