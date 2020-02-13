from rest_framework import routers
from django.urls import include, path
from .viewsets.version_viewset import ApiVersion
from ...eol_servico.urls import router as servico_eol_router
from ...alunos.urls import router as aluno_router

# Importe aqui as rotas das demais aplicações

router = routers.DefaultRouter()

router.register('api/version', ApiVersion, basename='Version')

# Adicione aqui as rotas das demais aplicações para que as urls sejam exibidas na API Root do DRF
# Adicione aqui as rotas das demais aplicações para que as urls sejam exibidas na API Root do DRF
router.registry.extend(servico_eol_router.registry)
router.registry.extend(aluno_router.registry)

urlpatterns = [
    path('', include(router.urls))
]
