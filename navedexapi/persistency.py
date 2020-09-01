from django.contrib.auth.models import User

from navedexapi.models import Naver, Project


def retrieve_all_navers(query_params_filters: dict, user_id: int):
    """
    Returns all objects of type Naver

    #Parameters:
        query_params_filters (dict):The list of query params passed in the request
        user_id (int):User unique identifier

    #Returns:
        retrieved_navers_list (list):List of Naver objects created by the user who made the request
    """

    retrieved_navers_list = Naver.objects.filter(created_by_user=user_id, **query_params_filters)

    return retrieved_navers_list


def retrieve_all_projects(query_params_filters: dict, user_id: int):
    """
    Returns all objects of type Project

    #Parameters:
        query_params_filters (dict):The list of query params passed in the request
        user_id (int):User unique identifier

    #Returns:
        retrieved_projects_list (list):List of Project objects created by the user who made the request
    """
    retrieved_projects_list = Project.objects.filter(created_by_user=user_id, **query_params_filters)

    return retrieved_projects_list


def retrieve_naver(naver_id: int, user_id: int):
    """
    Returns a specific Naver object, searched by ID

    #Parameters:
        naver_id (int):Naver unique identifier
        user_id (int):User unique identifier

    #Returns:
        retrieved_naver (Naver):Object of type Naver that has the given ID.
    """
    retrieved_naver = Naver.objects.filter(id=naver_id, created_by_user=user_id)

    return retrieved_naver


def retrieve_project(project_id: int, user_id: int):
    """
    Returns a specific Project object, searched by ID

    #Parameters:
        project_id (int):Project unique identifier
        user_id (int):User unique identifier

    #Returns:
        retrieved_project (Project):Object of type Project that has the given ID.
    """
    retrieved_project = Project.objects.filter(id=project_id, created_by_user=user_id)

    return retrieved_project


def retrieve_naver_projects(projects_list: list):
    """
    Returns the list of projects for a specific Naver.

    #Parameters:
        projects_list (list):List of project identifiers for a Naver

    #Returns:
        retrieved_projects (list):List of objects of type Project to which a specific Naver is part.
    """
    retrieved_projects = Project.objects.filter(id__in=projects_list)
    return retrieved_projects


def retrieve_project_navers(navers_list: list):
    """
    Returns the list of navers for a specific Project.

    #Parameters:
        navers_list (list):List of navers identifiers for a Project

    #Returns:
        retrieved_navers (list):List of Naver objects that are part of a specific Project.
    """
    retrieved_navers = Naver.objects.filter(id__in=navers_list)
    return retrieved_navers


def create_naver(request_body: dict, request_user: User):
    """
    Creates a new object of type Naver.

    #Parameters:
        request_body (dict):Body in JSON format with the necessary fields for creating a new Naver.
        request_user (User):User type object that represents the user who made the request.

    #Returns:
        created_naver (Naver):New object of type Naver created.
    """
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
    """
    Creates a new object of type Project.

    #Parameters:
        request_body (dict):Body in JSON format with the necessary fields for creating a new Project.
        request_user (User):User type object that represents the user who made the request.

    #Returns:
        created_project(Project):New object of type Project created.
    """
    created_project = Project.objects.create(
        name=request_body.get('name'),
        navers=request_body.get('navers'),
        created_by_user=request_user.id
    )

    return created_project


def update_retrieved_naver(request_body: dict, retrieved_naver: Naver):
    """
    Update an object of type Naver.

    #Parameters:
        request_body (dict):Body in JSON format with the necessary fields for update a Naver.
        retrieved_naver (Naver):Existing object of type Naver.

    #Returns:
        retrieved_naver (Naver):Updated object of type Naver.
    """
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
    """
    Update an object of type Project.

    #Parameters:
        request_body (dict):Body in JSON format with the necessary fields for update a Project.
        retrieved_project (Project):Existing object of type Project.

    #Returns:
        retrieved_project (Project):Updated object of type Project.
    """
    if request_body.get('name'):
        retrieved_project.name = request_body.get('name')
    if request_body.get('navers'):
        retrieved_project.navers = request_body.get('navers')

    retrieved_project.save()

    return retrieved_project


def delete_retrieved_naver(retrieved_naver: Naver):
    """
    Delete an object of type Naver.

    #Parameters:
        retrieved_naver (Naver):Existing object of type Naver.

    """
    retrieved_naver.delete()
    return


def delete_retrieved_project(retrieved_project: Project):
    """
    Delete an object of type Project.

    #Parameters:
        retrieved_project (Project):Existing object of type Project.

    """
    retrieved_project.delete()
    return
