# Generated by Django 5.1.2 on 2024-10-22 10:14

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Premium Plan', max_length=100)),
                ('price_monthly', models.DecimalField(decimal_places=2, default=10.0, max_digits=6)),
                ('price_yearly', models.DecimalField(decimal_places=2, default=100.0, max_digits=6)),
                ('price_two_years', models.DecimalField(decimal_places=2, default=180.0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.CharField(choices=[('M', 'Monthly'), ('Y', 'Yearly'), ('2Y', '2 Years')], default='M', max_length=2)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_date', models.DateTimeField()),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription.subscriptionplan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
