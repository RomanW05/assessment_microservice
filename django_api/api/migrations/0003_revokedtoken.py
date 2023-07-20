# Generated by Django 4.2.3 on 2023-07-19 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_blacklistedtoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='RevokedToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Revoked Tokens',
            },
        ),
    ]