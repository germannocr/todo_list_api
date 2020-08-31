import json

from django.http import JsonResponse
from rest_framework import status

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from navedexapi.exceptions import NaverNotFound, ProjectNotFound
from navedexapi.mappers import map_get_naver_response, map_post_naver_response, map_delete_naver_response, \
    map_get_project_response, map_post_project_response, map_patch_naver_response, map_patch_project_response, \
    map_delete_project_response, prepare_company_time_filter
from navedexapi.persistency import retrieve_all_navers, retrieve_naver, retrieve_naver_projects, create_naver, \
    update_retrieved_naver, delete_retrieved_naver, retrieve_all_projects, retrieve_project, retrieve_project_navers, \
    create_project, update_retrieved_project, delete_retrieved_project
from navedexapi.serializers import NaverSerializer, ProjectSerializer

from navedexapi.validations import validate_naver_post_body, validate_naver_query_params, validate_object_id, \
    validate_project_query_params, validate_project_post_body


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_naver(request, naver_id: int):
    validate_object_id(naver_id)
    user = request.user
    try:
        retrieved_naver = retrieve_naver(naver_id=naver_id, user_id=user.id)

        if retrieved_naver:
            delete_retrieved_naver(retrieved_naver=retrieved_naver[0])
            mapped_response = map_delete_naver_response()
            return mapped_response
        else:
            raise NaverNotFound(code=404)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_naver(request, naver_id: int):
    request_body = json.loads(request.body)
    validate_object_id(naver_id)
    user = request.user
    try:
        retrieved_naver = retrieve_naver(naver_id=naver_id, user_id=user.id)
        if retrieved_naver:
            updated_naver = update_retrieved_naver(request_body=request_body,
                                                   retrieved_naver=retrieved_naver[0])
            serializer_response = NaverSerializer(updated_naver)
            mapped_response = map_patch_naver_response(serializer_response)
            return mapped_response
        else:
            raise NaverNotFound(code=404)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_naver(request):
    request_body = json.loads(request.body)
    user = request.user
    try:
        validate_naver_post_body(request_body=request_body)
        new_naver = create_naver(request_body=request_body,
                                 request_user=user)
        serializer_response = NaverSerializer(new_naver)
        mapped_response = map_post_naver_response(serializer_response)
        return mapped_response
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_navers_list(request):
    query_params_filters = request.query_params
    query_params_filters = validate_naver_query_params(query_params_filters)
    user = request.user
    try:
        retrieved_navers_list = retrieve_all_navers(query_params_filters=query_params_filters, user_id=user.id)
        serialized_response = NaverSerializer(retrieved_navers_list, many=True)
        return map_get_naver_response(serialized_response)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_naver_by_id(request, naver_id: int):
    validate_object_id(naver_id)
    user = request.user
    try:
        retrieved_naver = retrieve_naver(naver_id=naver_id, user_id=user.id)
        if retrieved_naver:
            retrieved_projects = retrieve_naver_projects(projects_list=retrieved_naver[0].projects)
            serialized_response = NaverSerializer(retrieved_naver, many=True)
            return map_get_naver_response(serialized_response, retrieved_projects)
        else:
            raise NaverNotFound(code=404)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_project_by_id(request, project_id: int):
    validate_object_id(project_id)
    user = request.user
    try:
        retrieved_project = retrieve_project(project_id=project_id, user_id=user.id)
        if retrieved_project:
            retrieved_navers = retrieve_project_navers(navers_list=retrieved_project.navers)
            serialized_response = ProjectSerializer(retrieved_project, many=True)
            return map_get_project_response(serialized_response=serialized_response, navers_list=retrieved_navers)
        else:
            raise ProjectNotFound(code=404)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_projects_list(request):
    query_params_filters = request.query_params
    validate_project_query_params(query_params=query_params_filters)
    user = request.user
    try:
        retrieved_projects_list = retrieve_all_projects(query_params_filters=query_params_filters, user_id=user.id)

        serialized_response = ProjectSerializer(retrieved_projects_list, many=True)
        return map_get_project_response(serialized_response)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_project(request):
    request_body = json.loads(request.body)
    user = request.user
    try:
        validate_project_post_body(request_body=request_body)
        new_project = create_project(request_body=request_body,
                                     request_user=user)
        serializer_response = ProjectSerializer(new_project)
        mapped_response = map_post_project_response(serializer_response)
        return mapped_response
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_project(request, project_id: int):
    request_body = json.loads(request.body)
    validate_object_id(project_id)
    user = request.user
    try:
        retrieved_project = retrieve_project(project_id=project_id, user_id=user.id)
        if retrieved_project:
            updated_project = update_retrieved_project(request_body=request_body,
                                                       retrieved_project=retrieved_project)
            serializer_response = ProjectSerializer(updated_project)
            mapped_response = map_patch_project_response(serializer_response)
            return mapped_response
        else:
            raise ProjectNotFound(code=404)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_project(request, project_id: int):
    validate_object_id(project_id)
    user = request.user

    try:
        retrieved_project = retrieve_project(project_id=project_id, user_id=user.id)

        if retrieved_project:
            delete_retrieved_project(retrieved_project=retrieved_project)
            mapped_response = map_delete_project_response()
            return mapped_response
        else:
            raise ProjectNotFound(code=404)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
