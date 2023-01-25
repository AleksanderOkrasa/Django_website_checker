# Generated by Django 4.1.5 on 2023-01-11 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebpageData',
            fields=[
                ('name_webpage', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('available', 'Available'), ('notAvailable', 'Not Available')], default='notAvailable', max_length=30)),
                ('first_search_user', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('count_of_search', models.IntegerField(default=1, verbose_name='count of search')),
                ('buttons', models.IntegerField(null=True)),
                ('links', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('user_web', models.CharField(max_length=510, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=255)),
                ('count_of_search', models.IntegerField(default=1)),
                ('webpage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.webpagedata')),
            ],
        ),
    ]
