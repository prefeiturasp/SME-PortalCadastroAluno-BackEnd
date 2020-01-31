from rest_framework import routers
from django.urls import include, path
from .viewsets.version_viewset import ApiVersion

# Importe aqui as rotas das demais aplicações

router = routers.DefaultRouter()

router.register('api/version', ApiVersion, basename='Version')

# Adicione aqui as rotas das demais aplicações para que as urls sejam exibidas na API Root do DRF

urlpatterns = [
    path('', include(router.urls))
]
