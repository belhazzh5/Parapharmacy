# Generated by Django 3.2.8 on 2022-02-22 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_commandeitem_favorable_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commandeitem',
            name='quantite',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
