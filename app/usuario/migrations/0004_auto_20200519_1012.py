# Generated by Django 2.2.6 on 2020-05-19 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_auto_20200518_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genero',
            name='genero',
            field=models.CharField(default='Prefiero no decir', max_length=15),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='genero',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='usuario.Genero'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='rol_usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='usuario.TipoUsuario'),
        ),
    ]
