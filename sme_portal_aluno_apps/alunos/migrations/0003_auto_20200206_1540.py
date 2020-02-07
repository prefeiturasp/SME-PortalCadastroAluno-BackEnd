# Generated by Django 2.2.9 on 2020-02-06 18:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alunos', '0002_logconsultaeol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='codigo_eol',
            field=models.CharField(max_length=7, unique=True, validators=[django.core.validators.MinLengthValidator(7)], verbose_name='Código EOL do Aluno'),
        ),
    ]