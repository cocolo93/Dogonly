# Generated by Django 5.1 on 2024-10-01 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogonly_app', '0005_post_image_post_image_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]