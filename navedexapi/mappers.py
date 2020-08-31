from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from rest_framework import status

from navedexapi.serializers import NaverSerializer, ProjectSerializer


def map_delete_naver_response():
    return JsonResponse(
        None,
        safe=False,
        status=status.HTTP_204_NO_CONTENT
    )


def map_delete_project_response():
    return JsonResponse(
        None,
        safe=False,
        status=status.HTTP_204_NO_CONTENT
    )


def map_patch_naver_response(serialized_response):
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_200_OK
    )


def map_post_naver_response(serialized_response):
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_201_CREATED
    )


def map_post_project_response(serialized_response):
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_201_CREATED
    )


def map_patch_project_response(serialized_response):
    return JsonResponse(
        {
            'content': serialized_response.data
        },
        safe=False,
        status=status.HTTP_201_CREATED
    )


def map_get_naver_response(serialized_response: NaverSerializer, projects_list: list = None):
    if projects_list:
        serialized_response.data["projects"] = []
        for current_project in projects_list:
            serialized_response.data["projects"].append(
                {
                    "id": current_project.id,
                    "name": current_project.name
                }
            )

        return JsonResponse(
            {
                'content': serialized_response.data
            },
            safe=False,
            status=status.HTTP_200_OK
        )
    else:
        del serialized_response.data['projects']
        return JsonResponse(
            {
                'content': serialized_response.data
            },
            safe=False,
            status=status.HTTP_200_OK
        )


def map_get_project_response(serialized_response: ProjectSerializer, navers_list: list = None):
    if navers_list:
        serialized_response.data["navers"] = []
        for current_naver in navers_list:
            serialized_response.data["navers"].append(
                {
                    "id": current_naver.id,
                    "name": current_naver.name,
                    "birthdate": current_naver.birthdate,
                    "admission-date": current_naver.admission_date,
                    "job-role": current_naver.job_role
                }
            )

        return JsonResponse(
            {
                'content': serialized_response.data
            },
            safe=False,
            status=status.HTTP_200_OK
        )
    else:
        del serialized_response.data['navers']
        return JsonResponse(
            {
                'content': serialized_response.data
            },
            safe=False,
            status=status.HTTP_200_OK
        )