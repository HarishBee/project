# Generated by Django 5.0.4 on 2024-05-01 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('babapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='forget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=254)),
                ('OTP', models.IntegerField(max_length=4)),
            ],
        ),
    ]
