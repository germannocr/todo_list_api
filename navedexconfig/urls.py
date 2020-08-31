"""navedex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import refresh_jwt_token, obtain_jwt_token

from navedexapi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', include('rest_auth.registration.urls')),
    url(r'^refresh-token/', refresh_jwt_token),
    url(r'^login/', obtain_jwt_token),

    url(r'^createnaver/$', views.add_naver, name='post_naver'),
    url(r'^getnaverslist/$', views.retrieve_navers_list, name='get_all_navers'),
    path('getnaver/<int:naver_id>/', views.retrieve_naver_by_id, name='get_naver_by_id'),
    path('updatenaver/<int:naver_id>', views.update_naver, name='update_naver'),
    path('deletenaver/<int:naver_id>', views.delete_naver, name='delete_naver'),

    url(r'^createproject/$', views.add_project, name='post_project'),
    url(r'^getprojectlist/$', views.retrieve_projects_list, name='get_all_projects'),
    path('getproject/<int:project_id>/', views.retrieve_project_by_id, name='get_project_by_id'),
    path('updateproject/<int:project_id>', views.update_project, name='update_project'),
    path('deleteproject/<int:project_id>', views.delete_project, name='delete_project')
]

