# import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="address",
            field=models.CharField(default="Не указан", max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="notes",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="order",
            name="phone",
            field=models.CharField(default="Не указан", max_length=15),
            preserve_default=False,
        ),
    ]
