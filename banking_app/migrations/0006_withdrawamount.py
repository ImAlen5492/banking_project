# Generated by Django 4.2.2 on 2023-07-10 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banking_app', '0005_ministatement'),
    ]

    operations = [
        migrations.CreateModel(
            name='withdrawamount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
    ]
