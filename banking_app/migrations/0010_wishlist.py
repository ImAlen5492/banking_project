# Generated by Django 4.2.2 on 2023-07-21 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking_app', '0009_addamount_uid_withdrawamount_uid'),
    ]

    operations = [
        migrations.CreateModel(
            name='wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=300)),
                ('content', models.CharField(max_length=5000)),
                ('date', models.DateField()),
            ],
        ),
    ]
