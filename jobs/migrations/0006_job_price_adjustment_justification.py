# Generated by Django 4.1.7 on 2023-11-05 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_job_extra_discount_pecentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='price_adjustment_justification',
            field=models.TextField(blank=True, default='No note left', max_length=2500, null=True),
        ),
    ]