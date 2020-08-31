from django.contrib.auth.models import User

from navedexapi.models import Naver, Project


def retrieve_all_navers(query_params_filters: dict, user_id: int):
    retrieved_navers_list = Naver.objects.filter(created_by_user=user_id, **query_params_filters)

    return retrieved_navers_list


def retrieve_all_projects(query_params_filters: dict, user_id: int):
    retrieved_projects_list = Project.objects.filter(created_by_user=user_id, **query_params_filters)

    return retrieved_projects_list


def retrieve_naver(naver_id: int, user_id: int):
    retrieved_naver = Naver.objects.filter(id=naver_id, created_by_user=user_id)

    return retrieved_naver


def retrieve_project(project_id: int, user_id: int):
    retrieved_project = Project.objects.filter(id=project_id, created_by_user=user_id)

    return retrieved_project


def retrieve_naver_projects(projects_list: list):
    retrieved_projects = Project.objects.filter(id__in=projects_list)
    return retrieved_projects


def retrieve_project_navers(navers_list: list):
    retrieved_navers = Naver.objects.filter(id__in=navers_list)
    return retrieved_navers


def create_naver(request_body: dict, request_user: User):
    created_naver = Naver.objects.create(
        name=request_body.get('name'),
        birthdate=request_body.get('birthdate'),
        admission_date=request_body.get('admission_date'),
        job_role=request_body.get('job_role'),
        projects=request_body.get('projects'),
        created_by_user=request_user.id
    )

    return created_naver


def create_project(request_body: dict, request_user: User):
    created_project = Project.objects.create(
        name=request_body.get('name'),
        navers=request_body.get('navers'),
        created_by_user=request_user.id
    )

    return created_project


def update_retrieved_naver(request_body: dict, retrieved_naver: Naver):
    if request_body.get('name'):
        retrieved_naver.name = request_body.get('name')
    if request_body.get('birthdate'):
        retrieved_naver.birthdate = request_body.get('birthdate')
    if request_body.get('admission_date'):
        retrieved_naver.admission_date = request_body.get('admission_date')
    if request_body.get('job_role'):
        retrieved_naver.job_role = request_body.get('job_role')
    if request_body.get('projects'):
        retrieved_naver.projects = request_body.get('projects')
    retrieved_naver.save()

    return retrieved_naver


def update_retrieved_project(request_body: dict, retrieved_project: Project):
    if request_body.get('name'):
        retrieved_project.name = request_body.get('name')
    if request_body.get('navers'):
        retrieved_project.navers = request_body.get('navers')

    retrieved_project.save()

    return retrieved_project


def delete_retrieved_naver(retrieved_naver: Naver):
    retrieved_naver.delete()
    return


def delete_retrieved_project(retrieved_project: Project):
    retrieved_project.delete()
    return
