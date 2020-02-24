# Generated by Django 2.2.9 on 2020-02-23 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='codigo_dre',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Código EOL da DRE'),
        ),
        migrations.AddField(
            model_name='user',
            name='codigo_escola',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Código EOL da Escola'),
        ),
    ]