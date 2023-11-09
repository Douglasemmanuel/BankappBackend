# Generated by Django 4.0 on 2023-11-09 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0003_account_sort_code_alter_account_account_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='iban',
            field=models.CharField(default=1, max_length=22, unique=True),
            preserve_default=False,
        ),
    ]