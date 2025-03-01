# Generated by Django 5.1.3 on 2025-02-19 11:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_ad'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ad',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='ad',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='ad',
            name='status',
            field=models.CharField(choices=[('draft', 'Черновик'), ('published', 'Опубликовано'), ('hidden', 'Скрыто')], default='draft', max_length=10),
        ),
        migrations.AddField(
            model_name='ad',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
