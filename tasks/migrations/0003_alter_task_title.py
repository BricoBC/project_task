# Generated by Django 4.2.7 on 2023-11-10 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_task_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(default='', max_length=200),
        ),
    ]
