# Generated by Django 3.1.3 on 2020-11-07 03:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('artigo', '0005_auto_20201107_0051'),
        ('aluguel', '0005_auto_20201107_0051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluguel',
            name='tipo_prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artigo.tipodeproduto'),
        ),
    ]