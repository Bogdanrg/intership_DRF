# Generated by Django 4.2.3 on 2023-07-13 10:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("auto_orders", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="autoorder",
            name="total_sum",
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=20),
        ),
    ]
