# Generated by Django 3.2.18 on 2023-04-03 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0004_alter_endpoint_required_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callresult',
            name='error',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='callresult',
            name='result_json',
            field=models.JSONField(null=True),
        ),
    ]