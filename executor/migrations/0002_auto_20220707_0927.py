# Generated by Django 3.1.14 on 2022-07-07 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('executor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='nessus_scan_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='scan',
            name='nessus_scan_name',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
