# Generated by Django 5.0.2 on 2024-03-15 18:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_image_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image_thumbnail',
        ),
    ]
