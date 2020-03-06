from django.contrib.postgres import fields
from django_json_widget.widgets import JSONEditorWidget

from django.contrib import admin

from .models import (Aluno, Responsavel, LogConsultaEOL)
from .forms import LogConsultaEOLForm


class AlunoInLine(admin.StackedInline):
    model = Aluno
    extra = 0  # Quantidade de linhas que serão exibidas.


class ResponsavelInLine(admin.StackedInline):
    model = Responsavel
    extra = 0  # Quantidade de linhas que serão exibidas.


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    def ultima_alteracao(self, obj):
        return obj.alterado_em.strftime("%d/%m/%Y %H:%M:%S")

    ultima_alteracao.admin_order_field = 'alterado_em'
    ultima_alteracao.short_description = 'Última alteração'

    def celular(self, obj):
        if obj.responsavel.ddd_celular and obj.responsavel.celular:
            return obj.responsavel.ddd_celular + ' ' + obj.responsavel.celular
        else:
            return f'Celular incompleto'

    def nome_responsavel(self, obj):
        return obj.responsavel.nome

    nome_responsavel.short_descriptions = 'Nome do Responsavel'

    def cpf_responsavel(self, obj):
        return obj.responsavel.cpf

    cpf_responsavel.short_descriptions = 'CPF do Responsavel'

    list_display = ('nome', 'codigo_eol', 'data_nascimento', 'nome_responsavel',
                    'cpf_responsavel', 'celular')
    ordering = ('-alterado_em',)
    search_fields = ('codigo_eol', 'nome', 'responsavel__cpf', 'responsavel__nome')
    list_filter = ('responsavel__status',)


@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    inlines = [AlunoInLine]

    def ultima_alteracao(self, obj):
        return obj.alterado_em.strftime("%d/%m/%Y %H:%M:%S")

    ultima_alteracao.admin_order_field = 'alterado_em'
    ultima_alteracao.short_description = 'Última alteração'

    def celular(self, obj):
        return obj.ddd_celular + ' ' + obj.celular

    def enviar_emails(self, request, queryset):
        for responsavel in queryset.all():
            responsavel.enviar_email()
        self.message_user(request, 'E-mails enviados com sucesso.')

    enviar_emails.short_description = 'Enviar email para responsaveis'

    list_display = ('nome', 'cpf', 'data_nascimento', 'vinculo', 'nome_mae', 'celular', 'email', 'status')
    ordering = ('-alterado_em',)
    search_fields = ('uuid', 'cpf', 'nome')
    list_filter = ('status',)
    actions = ['enviar_emails', ]


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
