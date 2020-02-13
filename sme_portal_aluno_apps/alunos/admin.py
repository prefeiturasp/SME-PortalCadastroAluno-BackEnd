from django.contrib.postgres import fields
from django_json_widget.widgets import JSONEditorWidget

from django.contrib import admin

from .models import (Aluno, Responsavel, LogConsultaEOL)
from .forms import LogConsultaEOLForm


class AlunoInLine(admin.StackedInline):
    model = Aluno
    extra = 1  # Quantidade de linhas que serão exibidas.


@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    def ultima_alteracao(self, obj):
        return obj.alterado_em.strftime("%d/%m/%Y %H:%M:%S")

    ultima_alteracao.admin_order_field = 'alterado_em'
    ultima_alteracao.short_description = 'Última alteração'

    def celular(self, obj):
        return obj.ddd_celular + ' ' + obj.celular

    list_display = ('nome', 'cpf', 'data_nascimento', 'vinculo', 'nome_mae', 'celular', 'email', 'status')
    ordering = ('-alterado_em',)
    search_fields = ('uuid', 'cpf', 'nome')
    list_filter = ('status',)
    inlines = [AlunoInLine]


@admin.register(LogConsultaEOL)
class LogConsultaEOLAdmin(admin.ModelAdmin):
    form = LogConsultaEOLForm
    list_display = ('codigo_eol', 'criado_em',)
    search_fields = ('codigo_eol',)
    readonly_fields = ('criado_em',)
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }
    fields = ('codigo_eol', 'criado_em', 'json')
    fieldsets = (
    )
