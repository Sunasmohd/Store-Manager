# Generated by Django 4.2.6 on 2023-10-31 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_remove_customer_email_remove_customer_first_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'permissions': [('view_history', 'Can View History')]},
        ),
    ]
