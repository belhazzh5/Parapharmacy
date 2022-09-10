# Generated by Django 4.0.2 on 2022-02-15 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_subcategory_category_subcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='subcategory',
        ),
        migrations.AddField(
            model_name='category',
            name='subcategory',
            field=models.ManyToManyField(blank=True, null=True, to='store.Subcategory'),
        ),
    ]