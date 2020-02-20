from django.contrib import admin

from .models import ListaPalavrasBloqueadas


@admin.register(ListaPalavrasBloqueadas)
class ListaPalavrasBloqueadasAdmin(admin.ModelAdmin):
    list_display = ('palavra', 'criado_em',)
    search_fields = ('palavra',)
