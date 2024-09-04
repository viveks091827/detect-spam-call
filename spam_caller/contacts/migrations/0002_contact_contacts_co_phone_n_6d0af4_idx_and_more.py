# Generated by Django 5.1 on 2024-08-25 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contacts", "0001_initial"),
        ("users", "0002_profile_users_profi_phone_n_8821cb_idx"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="contact",
            index=models.Index(
                fields=["phone_number"], name="contacts_co_phone_n_6d0af4_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="spam_number",
            index=models.Index(
                fields=["phone_number"], name="contacts_sp_phone_n_b140a6_idx"
            ),
        ),
    ]
