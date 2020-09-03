import logging

from ..models.responsavel import Responsavel


log = logging.getLogger(__name__)


class ProcessarRetornoService(object):

    @classmethod
    def processar_credito_concedido(cls, codigo_eol):
        log.info(f"Inicia processo de atualização para crédito concedido")
        try:
            responsavel = Responsavel.objects.get(codigo_eol_aluno=codigo_eol)
            responsavel.status = Responsavel.STATUS_CREDITO_CONCEDIDO
            responsavel.save()
            log.info(f"Aluno {codigo_eol} atualizado para crédito concedido")

        except Responsavel.DoesNotExist:
            log.info(f"Codigo eol informado: {codigo_eol}, não possui responsavel.")

    @classmethod
    def processar_todos_credito_consedido(cls):
        from ..models.retorno_mp import RetornoMP
        try:
            retornos = RetornoMP.objects.filter(
                registro_processado=False, status=RetornoMP.STATUS_CREDITADO).values_list('codigo_eol', flat=True)
            Responsavel.objects.filter(codigo_eol_aluno__in=retornos).update(status=Responsavel.STATUS_CREDITO_CONCEDIDO)
            retornos.update(registro_processado=True)
        except Exception as e:
            log.error('Falha no processamento: ' + str(e))
