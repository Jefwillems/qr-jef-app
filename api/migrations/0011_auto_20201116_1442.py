# Generated by Django 3.1.3 on 2020-11-16 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20201104_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=128, unique=True),
        ),
    ]
