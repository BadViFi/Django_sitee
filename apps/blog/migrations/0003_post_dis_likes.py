# Generated by Django 5.0.2 on 2024-02-23 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_image_alter_post_is_published_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dis_likes',
            field=models.IntegerField(blank=True, default=0, verbose_name='Огидайки'),
        ),
    ]
