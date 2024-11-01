# Generated by Django 5.1 on 2024-09-12 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogonly_app', '0004_user_image_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='contents/'),
        ),
        migrations.AddField(
            model_name='post',
            name='image_hash',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
    ]
