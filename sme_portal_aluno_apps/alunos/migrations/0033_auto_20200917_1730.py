# Generated by Django 2.2.9 on 2020-09-17 20:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alunos', '0032_logerroatualizacaoeol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logerroatualizacaoeol',
            name='cpf',
            field=models.CharField(blank=True, max_length=11, null=True, validators=[django.core.validators.RegexValidator(message='Necessário 11 digitos', regex='^\\d{11}$')], verbose_name='CPF do Responsável'),
        ),
    ]
