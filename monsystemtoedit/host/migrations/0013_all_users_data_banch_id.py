# Generated by Django 3.1.7 on 2023-04-22 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host', '0012_auto_20230422_0128'),
    ]

    operations = [
        migrations.AddField(
            model_name='all_users_data',
            name='banch_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]