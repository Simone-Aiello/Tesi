# Generated by Django 4.0.3 on 2022-04-22 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest_api', '0007_alter_measurement_sensor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='data',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]