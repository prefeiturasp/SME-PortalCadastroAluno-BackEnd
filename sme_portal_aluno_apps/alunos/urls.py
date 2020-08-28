from django.urls import path, include
from rest_framework import routers

from .api.viewsets.alunos_viewset import AlunosViewSet
from .api.viewsets.retorno_mp_viewset import RetornoMPViewset

router = routers.DefaultRouter()

router.register('alunos', AlunosViewSet)
router.register('retorno-mp', RetornoMPViewset)

urlpatterns = [
    path('', include(router.urls)),
]
