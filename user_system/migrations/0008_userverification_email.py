# Generated by Django 4.0.3 on 2022-06-22 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_system', '0007_userverification_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='userverification',
            name='email',
            field=models.CharField(default='', max_length=20),
        ),
    ]
