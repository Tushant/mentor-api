# Generated by Django 2.1.5 on 2019-03-10 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20190310_0217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='achievement',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievement', to='accounts.Profile'),
        ),
    ]
