# Generated by Django 4.2.1 on 2023-06-06 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.BinaryField(editable=True),
        ),
    ]
