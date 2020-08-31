from rest_framework import serializers

from navedexapi.models import Naver, Project


class NaverSerializer(serializers.ModelSerializer):

    class Meta:
        model = Naver
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'
