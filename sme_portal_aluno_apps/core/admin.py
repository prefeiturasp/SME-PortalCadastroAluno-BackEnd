from django.contrib import admin

from .models import ListaPalavrasBloqueadas, Email, ListaEmail


@admin.register(ListaPalavrasBloqueadas)
class ListaPalavrasBloqueadasAdmin(admin.ModelAdmin):
    list_display = ('palavra', 'criado_em',)
    search_fields = ('palavra',)


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('enviar_para', 'criado_em', 'assunto', 'enviado')
    search_fields = ('enviar_para', 'criado_em', 'enviado')
    list_filter = ('enviado',)


@admin.register(ListaEmail)
class ListaEmailAdmin(admin.ModelAdmin):
    list_display = ('email',)
    search_fields = ('email',)
