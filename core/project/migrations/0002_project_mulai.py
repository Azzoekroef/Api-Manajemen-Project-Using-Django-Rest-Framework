# Generated by Django 5.0.1 on 2024-02-15 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='mulai',
            field=models.DateField(default="2024-02-14"),
            preserve_default=False,
        ),
    ]
