# Generated by Django 5.1.2 on 2024-10-21 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0008_watchhistory'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='watchhistory',
            unique_together=set(),
        ),
    ]
