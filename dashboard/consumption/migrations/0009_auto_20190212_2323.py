# Generated by Django 2.1.4 on 2019-02-12 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumption', '0008_auto_20190211_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumption',
            name='kWh',
            field=models.FloatField(db_index=True, default=0, verbose_name='kWh'),
        ),
    ]
