# Generated by Django 2.1.5 on 2019-03-10 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20190310_0216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='zip_code',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
