# Generated by Django 2.2.16 on 2022-02-03 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20220202_2234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genretitle',
            name='title',
        ),
        migrations.DeleteModel(
            name='Title',
        ),
    ]
