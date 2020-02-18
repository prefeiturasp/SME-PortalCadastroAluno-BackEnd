# Generated by Django 2.2.9 on 2020-02-10 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alunos', '0008_auto_20200208_1808'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='logconsultaeol',
            options={'verbose_name': 'Log Consulta EOL', 'verbose_name_plural': 'Logs Consultas EOL'},
        ),
        migrations.AlterField(
            model_name='aluno',
            name='responsavel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='alunos', to='alunos.Responsavel'),
        ),
    ]