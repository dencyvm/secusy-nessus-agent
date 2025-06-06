# Generated by Django 3.1.14 on 2022-07-04 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scan',
            fields=[
                ('scan_id', models.AutoField(primary_key=True, serialize=False)),
                ('target', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('scan_status', models.IntegerField(default='0')),
                ('result_url', models.CharField(blank=True, max_length=1000, null=True)),
                ('errors', models.CharField(blank=True, max_length=2000, null=True)),
            ],
        ),
    ]
