# Generated by Django 4.1.5 on 2023-01-22 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_alter_userdata_count_of_search_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webpagedata',
            name='name_webpage',
            field=models.CharField(max_length=1000, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='webpagedata',
            name='url',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
