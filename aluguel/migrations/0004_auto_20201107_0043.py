# Generated by Django 3.1.3 on 2020-11-07 03:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aluguel', '0003_auto_20201107_0018'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aluguel',
            options={'verbose_name_plural': 'Aluguéis'},
        ),
        migrations.AlterModelOptions(
            name='itemdealuguel',
            options={'verbose_name_plural': 'Itens De Aluguel'},
        ),
    ]
