from django.urls import path, include
from rest_framework import routers

from .api.viewsets.aluno_viewset import AlunosViewSet

router = routers.DefaultRouter()

router.register('alunos', AlunosViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
