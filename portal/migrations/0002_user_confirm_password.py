# Generated by Django 4.2.1 on 2024-02-21 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirm_password',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='confirm_password'),
        ),
    ]
