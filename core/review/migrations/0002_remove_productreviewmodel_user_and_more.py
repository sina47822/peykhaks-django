# Generated by Django 4.2 on 2024-09-10 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreviewmodel',
            name='user',
        ),
        migrations.AddField(
            model_name='productreviewmodel',
            name='name',
            field=models.CharField(default='sina', max_length=50),
            preserve_default=False,
        ),
    ]
