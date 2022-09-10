# Generated by Django 3.2.8 on 2022-02-22 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_auto_20220222_2203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commande',
            name='item',
        ),
        migrations.AddField(
            model_name='commande',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='commandeitem',
            name='commande',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.commande'),
        ),
        migrations.AddField(
            model_name='commandeitem',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]