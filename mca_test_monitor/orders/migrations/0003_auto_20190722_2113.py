# Generated by Django 2.2.3 on 2019-07-22 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_tests_and_combos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testtype',
            options={'ordering': ('position',)},
        ),
    ]
