# Generated by Django 5.1.7 on 2025-03-25 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Notify', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='user',
        ),
        migrations.AddField(
            model_name='notification',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
    ]
