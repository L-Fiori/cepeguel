# Generated by Django 3.1.3 on 2020-12-07 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aluguel', '0002_auto_20201207_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluguel',
            name='rented_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]
