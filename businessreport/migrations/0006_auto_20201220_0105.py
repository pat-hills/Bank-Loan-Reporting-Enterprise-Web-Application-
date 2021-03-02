# Generated by Django 3.1.1 on 2020-12-20 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessreport', '0005_auto_20201220_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthreport',
            name='report_value',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='monthreport',
            name='report_code',
            field=models.CharField(default='0000', max_length=128, null=True),
        ),
    ]
