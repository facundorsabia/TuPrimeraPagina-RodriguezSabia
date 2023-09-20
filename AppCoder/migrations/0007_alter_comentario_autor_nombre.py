# Generated by Django 4.2.5 on 2023-09-20 20:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('AppCoder', '0006_alter_publicacion_autor_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='autor_nombre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
