# Generated by Django 3.1.7 on 2021-04-19 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('U2H', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
