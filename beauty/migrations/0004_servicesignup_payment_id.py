# Generated by Django 4.2 on 2023-05-26 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("beauty", "0003_alter_servicetype_options_remove_servicesignup_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="servicesignup",
            name="payment_id",
            field=models.CharField(
                blank=True, max_length=100, verbose_name="Айди платежа"
            ),
        ),
    ]