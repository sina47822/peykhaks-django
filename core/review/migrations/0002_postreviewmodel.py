# Generated by Django 4.2 on 2025-01-01 12:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_post_avg_rate'),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostReviewModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('description', models.TextField()),
                ('rate', models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('status', models.IntegerField(choices=[(1, 'در انتظار تایید'), (2, 'تایید شده'), (3, 'رد شده')], default=1)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.post')),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
    ]
