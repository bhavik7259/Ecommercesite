# Generated by Django 3.1.2 on 2021-02-11 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Syssol', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
