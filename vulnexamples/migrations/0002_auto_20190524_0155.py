# Generated by Django 2.2.1 on 2019-05-23 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vulnexamples', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='hostsauthuser',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='hostsauthuser',
            name='subdomain',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]