# Generated by Django 3.1.3 on 2020-11-04 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20201025_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrcode',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.department'),
            preserve_default=False,
        ),
    ]