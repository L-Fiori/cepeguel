# Generated by Django 3.1.3 on 2020-12-05 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artigo', '0003_auto_20201204_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='pack',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='produto',
            name='foto',
            field=models.ImageField(max_length=300, upload_to='fotosdeartigo'),
        ),
    ]