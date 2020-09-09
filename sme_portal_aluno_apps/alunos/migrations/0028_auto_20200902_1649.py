# Generated by Django 2.2.9 on 2020-09-02 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alunos', '0027_auto_20200901_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responsavel',
            name='status',
            field=models.CharField(choices=[('ATUALIZADO_EOL', 'Cadastro Atualizado no EOL'), ('ATUALIZADO_VALIDO', 'Cadastro Atualizado e validado'), ('DIVERGENTE', 'Cadastro Divergente'), ('DESATUALIZADO', 'Cadastro Desatualizado'), ('PENDENCIA_RESOLVIDA', 'Cadastro com Pendência Resolvida'), ('CREDITO_CONCEDIDO', 'Cadastro com Crédito Concedido')], default='ATUALIZADO_VALIDO', max_length=30, verbose_name='status'),
        ),
    ]