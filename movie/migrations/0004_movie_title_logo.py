# Generated by Django 5.1.2 on 2024-10-20 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_remove_movie_director_movie_director'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='title_logo',
            field=models.ImageField(blank=True, null=True, upload_to='title_logo/'),
        ),
    ]
