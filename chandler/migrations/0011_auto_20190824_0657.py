# Generated by Django 2.2.4 on 2019-08-24 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chandler', '0010_auto_20190824_0655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderhistroy',
            name='amount',
            field=models.IntegerField(null=True),
        ),
    ]