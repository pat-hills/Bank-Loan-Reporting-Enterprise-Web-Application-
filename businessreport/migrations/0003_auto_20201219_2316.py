# Generated by Django 3.1.1 on 2020-12-19 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessreport', '0002_monthreport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthreport',
            name='report_value',
        ),
        migrations.AddField(
            model_name='monthreport',
            name='report_value_non_numeric',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='monthreport',
            name='report_value_numeric',
            field=models.IntegerField(null=True),
        ),
    ]