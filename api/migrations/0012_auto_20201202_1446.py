# Generated by Django 3.1.3 on 2020-12-02 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20201116_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apihit',
            name='action',
            field=models.CharField(choices=[('basic_info', 'Basic Info'), ('kiosk', 'Kiosk'), ('json', 'Json Response'), ('redirect', 'Redirect')], default='basic_info', max_length=16),
        ),
    ]