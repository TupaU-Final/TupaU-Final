# Generated by Django 2.2.6 on 2020-06-11 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0011_auto_20200528_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='descripcion_breve',
            field=models.TextField(default='No hay datos', verbose_name='Descripción Breve'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='hobbies',
            field=models.CharField(blank=True, default='No hay datos', max_length=150, null=True, verbose_name='Hobbies'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='situacion_sentimental',
            field=models.CharField(default='No hay datos', max_length=150, null=True, verbose_name='Situación Sentimental'),
        ),
        migrations.DeleteModel(
            name='InfoUsuario',
        ),
    ]
