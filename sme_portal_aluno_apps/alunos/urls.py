from django.urls import path, include
from rest_framework import routers


router = routers.DefaultRouter()

router.register('alunos')

urlpatterns = [
    path('', include(router.urls)),
]
