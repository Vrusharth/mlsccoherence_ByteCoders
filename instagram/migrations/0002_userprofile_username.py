# Generated by Django 3.2.1 on 2024-03-23 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='username',
            field=models.TextField(default='soham'),
            preserve_default=False,
        ),
    ]
