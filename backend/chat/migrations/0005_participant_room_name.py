# Generated by Django 3.1.1 on 2020-09-23 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20200923_0026'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='room_name',
            field=models.CharField(max_length=150, null=True),
        ),
    ]