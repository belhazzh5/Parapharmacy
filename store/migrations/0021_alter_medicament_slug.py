# Generated by Django 3.2.8 on 2022-02-22 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_alter_client_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicament',
            name='slug',
            field=models.SlugField(),
        ),
    ]