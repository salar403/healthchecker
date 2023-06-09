# Generated by Django 3.2.18 on 2023-04-10 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0006_alter_callresult_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='callresult',
            name='result_text',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='endpoint',
            name='response_type',
            field=models.IntegerField(choices=[(1, 'text'), (2, 'json'), (1, 'all')], default=2),
        ),
    ]
