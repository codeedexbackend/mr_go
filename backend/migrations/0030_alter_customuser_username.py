# Generated by Django 3.2.10 on 2024-03-22 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0029_auto_20240320_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
