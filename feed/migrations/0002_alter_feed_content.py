# Generated by Django 4.0.4 on 2022-06-04 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]