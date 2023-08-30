# Generated by Django 4.2.4 on 2023-08-28 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_profile_date_of_birth'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='main.post')),
            ],
        ),
    ]
