# Generated by Django 3.1.7 on 2023-04-10 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0002_members_cpu_usage'),
    ]

    operations = [
        migrations.AddField(
            model_name='members',
            name='cores',
            field=models.IntegerField(default=1),
        ),
    ]