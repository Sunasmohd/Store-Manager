# Generated by Django 5.0 on 2023-12-23 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_alter_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='promotions',
            field=models.ManyToManyField(null=True, to='store.promotion'),
        ),
    ]
