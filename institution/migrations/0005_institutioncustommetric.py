# Generated by Django 3.1.1 on 2020-12-09 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institution', '0004_auto_20201205_0310'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstitutionCustomMetric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metric_name', models.CharField(max_length=128)),
                ('metric_short_name', models.CharField(max_length=128, null=True)),
                ('unit_measurement', models.CharField(max_length=128)),
                ('preferred_chart', models.CharField(max_length=128, null=True)),
                ('description', models.CharField(max_length=128)),
                ('is_deleted', models.BooleanField(default=False)),
                ('date_created', models.DateField(auto_now=True)),
                ('date_time_created', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_created_by_metric', to=settings.AUTH_USER_MODEL)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institution_metric', to='institution.institution')),
            ],
        ),
    ]
