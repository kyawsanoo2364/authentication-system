# Generated by Django 5.2.1 on 2025-05-29 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_onetimepassword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onetimepassword',
            name='code',
            field=models.CharField(unique=True),
        ),
    ]
