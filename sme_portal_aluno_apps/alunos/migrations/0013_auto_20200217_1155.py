# Generated by Django 2.2.9 on 2020-02-17 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alunos', '0012_auto_20200217_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='responsavel',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alunos', to='alunos.Responsavel'),
        ),
    ]
