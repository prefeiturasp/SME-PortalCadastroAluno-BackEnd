import logging

from ..models.responsavel import Responsavel

log = logging.getLogger(__name__)


class ProcessarRetornoService(object):

    @classmethod
    def processar_todos_credito_consedido(cls):
        from ..models.retorno_mp import RetornoMP
        try:
            retornos = RetornoMP.objects.filter(
                registro_processado=False, status=RetornoMP.STATUS_CREDITADO).values_list('codigo_eol', flat=True)
            Responsavel.objects.filter(codigo_eol_aluno__in=retornos).update(
                status=Responsavel.STATUS_CREDITO_CONCEDIDO)
            retornos.update(registro_processado=True)
        except Exception as e:
            log.error('Falha no processamento: ' + str(e))

    @classmethod
    def cpf_invalido(cls, responsavel_id):
        log.info(f"Inicia processo de atualização para cpf invalido")
        try:
            responsavel = Responsavel.objects.get(id=responsavel_id)
            responsavel.status = Responsavel.STATUS_CPF_INVALIDO
            responsavel.save()
            log.info(f"responsavel pelo aluno {responsavel.codigo_eol_aluno} atualizado para cpf invalido")
            # TODO Chamar aqui rotina de envio de e-mail

        except Responsavel.DoesNotExist:
            log.info(f"Resposavel informado não existe na base")

    @classmethod
    def multiplos_emails(cls, responsavel_id):
        log.info(f"Inicia processo de atualização para multiplos e-mails")
        try:
            responsavel = Responsavel.objects.get(id=responsavel_id)
            responsavel.status = Responsavel.STATUS_MULTIPLOS_EMAILS
            responsavel.save()
            log.info(f"responsavel pelo aluno {responsavel.codigo_eol_aluno} atualizado para multiplos e-mails")
            # TODO Chamar aqui rotina de envio de e-mail

        except Responsavel.DoesNotExist:
            log.info(f"Resposavel informado não existe na base")
