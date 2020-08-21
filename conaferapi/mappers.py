from django.http import JsonResponse
from rest_framework import status


def map_post_response(serialized_response):
    return JsonResponse(
        {
            'post': serialized_response.data
        },
        safe=False,
        status=status.HTTP_201_CREATED
    )


def map_get_response(serialized_response):
    return JsonResponse(
        {
            'posts': serialized_response.data
        },
        safe=False,
        status=status.HTTP_200_OK
    )
