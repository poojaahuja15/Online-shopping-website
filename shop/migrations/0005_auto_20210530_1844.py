# Generated by Django 3.1.6 on 2021-05-30 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='address',
            new_name='address2',
        ),
        migrations.AddField(
            model_name='order',
            name='address1',
            field=models.CharField(default='', max_length=255),
        ),
    ]
