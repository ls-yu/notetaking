# Generated by Django 3.1.4 on 2021-03-28 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notetaking', '0004_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='date',
            field=models.CharField(max_length=10),
        ),
    ]
