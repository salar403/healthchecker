# Generated by Django 3.2.18 on 2023-03-15 13:14

import backend.customs.generators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='endpoint',
            name='convert_body_to_json',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='endpoint',
            name='recall_at',
            field=models.IntegerField(default=backend.customs.generators.current_int_timestamp),
        ),
        migrations.AlterField(
            model_name='callresult',
            name='state',
            field=models.IntegerField(choices=[(1, 'success'), (2, 'timeout'), (3, 'invalid_status'), (4, 'error')]),
        ),
    ]
