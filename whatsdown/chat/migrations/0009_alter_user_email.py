# Generated by Django 4.2.1 on 2023-06-06 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_chat_sent_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
