# Generated by Django 4.2.3 on 2023-07-12 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ams", "0002_userprofile_punchin"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="qr_image",
            field=models.URLField(default=""),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="profile_img",
            field=models.URLField(default=""),
        ),
    ]
