# Generated by Django 3.1.3 on 2020-11-07 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aluguel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_prod', models.CharField(max_length=100)),
                ('tipo_usr', models.CharField(max_length=100)),
                ('qtd', models.IntegerField()),
                ('hora', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ItemDeAluguel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
