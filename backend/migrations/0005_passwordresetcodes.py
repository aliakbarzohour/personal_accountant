# Generated by Django 4.1.7 on 2023-03-20 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_token_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passwordresetcodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=120)),
                ('time', models.DateField()),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]
