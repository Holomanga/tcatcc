# Generated by Django 3.0.5 on 2020-04-24 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tcatcc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='expiryDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
