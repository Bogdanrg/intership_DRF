# Generated by Django 4.2.3 on 2023-07-14 21:53

from django.db import migrations
import django_enum.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_alter_tradinguser_role_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradinguser',
            name='role',
            field=django_enum.fields.EnumCharField(blank=True, choices=[('admin', 'admin'), ('analyst', 'analyst'), ('default', 'default')], default='default', max_length=7),
        ),
    ]
