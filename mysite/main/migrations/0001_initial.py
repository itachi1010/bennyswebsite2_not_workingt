# Generated by Django 4.0.7 on 2023-01-23 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(max_length=150)),
                ('publication_year', models.IntegerField()),
                ('author', models.CharField(max_length=100)),
                ('plot', models.TextField()),
            ],
        ),
    ]
