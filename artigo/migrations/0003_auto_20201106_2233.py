# Generated by Django 3.1.3 on 2020-11-07 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artigo', '0002_auto_20201106_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='foto',
            field=models.FileField(upload_to='C:\\Users\\Gustavo\\cepeguel/fotos/fotosdeartigo'),
        ),
    ]
