# Generated by Django 2.1.5 on 2019-03-13 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190310_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'tyalent'), (2, 'trustee'), (3, 'company')], default=1),
        ),
    ]
