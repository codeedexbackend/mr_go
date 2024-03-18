# Generated by Django 3.2.10 on 2024-03-16 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_rename_business_description_customuser_business_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contactus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=30, null=True)),
                ('Email', models.EmailField(blank=True, max_length=254, null=True)),
                ('Mobile', models.IntegerField(blank=True, null=True)),
                ('Message', models.CharField(blank=True, max_length=3000, null=True)),
            ],
        ),
    ]