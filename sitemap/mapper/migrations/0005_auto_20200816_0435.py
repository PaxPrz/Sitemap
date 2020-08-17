# Generated by Django 3.1 on 2020-08-16 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapper', '0004_auto_20200812_0428'),
    ]

    operations = [
        migrations.AddField(
            model_name='vulnerability',
            name='request',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='vulnerability',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
