# Generated by Django 3.2.9 on 2021-11-25 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access', models.TextField()),
                ('refresh', models.TextField()),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('expires_in', models.IntegerField()),
            ],
        ),
    ]
