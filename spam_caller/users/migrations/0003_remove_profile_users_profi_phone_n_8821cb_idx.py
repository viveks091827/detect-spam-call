# Generated by Django 5.1 on 2024-08-25 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_profile_users_profi_phone_n_8821cb_idx"),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name="profile",
            name="users_profi_phone_n_8821cb_idx",
        ),
    ]
