# Generated by Django 2.2.9 on 2020-02-07 13:16

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alunos', '0004_auto_20200206_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logconsultaeol',
            name='json',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=[], verbose_name='Log'),
        ),
    ]