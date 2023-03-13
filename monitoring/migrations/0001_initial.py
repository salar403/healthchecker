# Generated by Django 3.2.18 on 2023-03-13 11:15

from django.db import migrations, models
import django.db.models.deletion
import unixtimestampfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0002_service_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Endpoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('base_url', models.URLField()),
                ('method', models.IntegerField(choices=[(1, 'get'), (2, 'post'), (3, 'put'), (4, 'delete')])),
                ('headers', models.JSONField(default=None)),
                ('body', models.JSONField(default=None)),
                ('query_params', models.JSONField(default=None)),
                ('healthy_status_code', models.IntegerField(default=200)),
                ('required_result', models.JSONField(default=None)),
                ('check_result_data', models.BooleanField(default=False)),
                ('timeout', models.IntegerField()),
                ('check_interval', models.IntegerField()),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='endpoints', to='user.user')),
            ],
        ),
        migrations.CreateModel(
            name='CallResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', unixtimestampfield.fields.UnixTimeStampField(auto_now_add=True)),
                ('response_time_ms', models.IntegerField()),
                ('status_code', models.IntegerField()),
                ('state', models.IntegerField(choices=[(1, 'success'), (2, 'timeout'), (3, 'invalid_status'), (4, 'error'), (5, 'unmatch_data')])),
                ('healthy', models.BooleanField()),
                ('error', models.TextField(default=None)),
                ('result_json', models.JSONField(default=None)),
                ('endpoint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='call_results', to='monitoring.endpoint')),
            ],
        ),
    ]
