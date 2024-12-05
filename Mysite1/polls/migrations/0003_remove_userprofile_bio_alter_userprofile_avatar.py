# Generated by Django 5.1.3 on 2024-11-22 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='bio',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
