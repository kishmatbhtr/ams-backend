# Generated by Django 4.2.3 on 2023-08-01 05:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ams', '0011_punchout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='punchin',
            name='checkin_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 5, 13, 21, 228824, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='punchout',
            name='checkout_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 1, 5, 13, 21, 229607, tzinfo=datetime.timezone.utc)),
        ),
    ]
