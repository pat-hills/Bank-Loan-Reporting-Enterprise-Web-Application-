# Generated by Django 3.1.1 on 2020-12-19 22:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_businesscustommetric'),
        ('institution', '0007_auto_20201210_1625'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('businessreport', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_code', models.CharField(max_length=128)),
                ('report_value', models.CharField(max_length=256)),
                ('report_category', models.CharField(max_length=256, null=True)),
                ('reporting_date', models.DateField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_created', models.DateField(auto_now=True)),
                ('date_time_created', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_month_report', to='business.business')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institution_month_report', to='institution.institution')),
                ('report_metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_metric', to='businessreport.reportmetric')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_month_report', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]