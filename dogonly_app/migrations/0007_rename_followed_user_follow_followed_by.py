# Generated by Django 4.2.16 on 2024-10-28 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dogonly_app", "0006_alter_post_created_at"),
    ]

    operations = [
        migrations.RenameField(
            model_name="follow",
            old_name="followed_user",
            new_name="followed_by",
        ),
    ]
