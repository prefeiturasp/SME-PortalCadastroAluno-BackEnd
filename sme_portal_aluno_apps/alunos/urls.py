from django.urls import path, include
from rest_framework import routers

# from .api.viewsets.alunos_viewset import AlunosViewSet
from .api.viewsets.responsaveis_viewset import ResponsaveisViewSet

router = routers.DefaultRouter()

router.register('responsaveis', ResponsaveisViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
