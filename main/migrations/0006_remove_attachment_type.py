# Generated by Django 4.2.4 on 2023-08-30 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_attachment_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='type',
        ),
    ]
