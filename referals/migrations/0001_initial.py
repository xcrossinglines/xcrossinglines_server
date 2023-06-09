# Generated by Django 4.1.7 on 2023-02-18 17:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Referal",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("referal_code", models.CharField(max_length=150, unique=True)),
                (
                    "referal_discount",
                    models.FloatField(blank=True, default=0.0, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "account",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
