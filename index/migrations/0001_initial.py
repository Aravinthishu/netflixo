# Generated by Django 5.1.2 on 2024-10-20 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('movie', '0002_movie_trailer'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movies', models.ManyToManyField(related_name='hero_sections', to='movie.movie')),
            ],
        ),
    ]
