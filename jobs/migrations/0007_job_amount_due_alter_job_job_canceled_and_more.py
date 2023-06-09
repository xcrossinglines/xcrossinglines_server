# Generated by Django 4.1.7 on 2023-04-14 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0006_alter_job_job_canceled_alter_job_job_completed"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="amount_due",
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="job_canceled",
            field=models.BooleanField(
                choices=[(False, "No"), (True, "Yes")], default=False
            ),
        ),
        migrations.AlterField(
            model_name="job",
            name="job_completed",
            field=models.BooleanField(
                choices=[(False, "No"), (True, "Yes")], default=False
            ),
        ),
    ]
