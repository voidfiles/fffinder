# Generated by Django 5.0.6 on 2024-06-19 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Page",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_created=True)),
                ("url", models.CharField(max_length=2000, unique=True)),
                ("domain", models.CharField(max_length=2000)),
                ("raw_url", models.CharField(max_length=2000)),
                ("content_hash", models.CharField(max_length=512, unique=True)),
                ("content", models.TextField(null=True)),
                ("title", models.TextField(null=True)),
                ("author", models.TextField(null=True)),
                ("content_date", models.DateTimeField(null=True)),
            ],
            options={
                "unique_together": {("url", "content_hash")},
            },
        ),
    ]
