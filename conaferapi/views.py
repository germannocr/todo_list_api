import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_condition import Or
from rest_framework import generics, status

# Create your views here.
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from conaferapi.mappers import map_post_response, map_get_response
from conaferapi.models import Post
from conaferapi.persistency import create_post
from conaferapi.serializers import PostSerializer

from conaferapi.validations import validate_post_body


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def add_posts(request):
    request_body = json.loads(request.body)
    user = request.user
    try:
        validate_post_body(request_body=request_body)
        new_post = create_post(request_body=request_body,
                               user=user)
        serializer_response = PostSerializer(new_post)
        mapped_response = map_post_response(serializer_response)
        return mapped_response
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        },
            safe=False,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def retrieve_posts(request):
    user = request.user.id
    posts = Post.objects.filter(created_by_user=user)
    serializer_response = PostSerializer(posts, many=True)
    return map_get_response(serializer_response)
