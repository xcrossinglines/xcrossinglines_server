# Generated by Django 4.1.7 on 2023-07-05 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0016_job_job_invoice_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_out_sourced',
            field=models.BooleanField(choices=[(False, 'No'), (True, 'Yes')], default=False),
        ),
        migrations.AlterField(
            model_name='job',
            name='referal_code',
            field=models.CharField(blank=True, default='xcrossinglines', max_length=150, null=True),
        ),
    ]
