# Generated by Django 2.2.9 on 2020-03-12 20:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListaEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('email', models.CharField(max_length=255, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Lista de Email',
                'verbose_name_plural': 'Lista de Emails',
            },
        ),
    ]
