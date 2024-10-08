# Generated by Django 5.0.7 on 2024-09-01 09:20

import django.core.validators
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AccountNumber",
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
                (
                    "account_number",
                    models.CharField(
                        max_length=12,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^\\d{12}$", "Account number must be exactly 12 digits."
                            )
                        ],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Bank_branches",
            fields=[
                ("branch_id", models.AutoField(primary_key=True, serialize=False)),
                ("branch_name", models.CharField(max_length=100)),
                ("state", models.CharField(blank=True, max_length=100, null=True)),
                ("city", models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                ("customer_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=60)),
                (
                    "phone_no",
                    models.CharField(
                        max_length=10,
                        unique=True,
                        validators=[django.core.validators.RegexValidator("^\\d{10}$")],
                    ),
                ),
                (
                    "Aadhar_no",
                    models.CharField(
                        max_length=12,
                        unique=True,
                        validators=[django.core.validators.RegexValidator("^\\d{12}$")],
                    ),
                ),
                ("DOB", models.DateField()),
                (
                    "password",
                    models.CharField(
                        max_length=128,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)"
                            )
                        ],
                    ),
                ),
                (
                    "account",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="myapp.accountnumber",
                    ),
                ),
                (
                    "branch_connect",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="myapp.bank_branches",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "account_id",
                    models.CharField(
                        default=uuid.uuid4,
                        editable=False,
                        max_length=36,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "account_type",
                    models.CharField(
                        choices=[("current", "Current"), ("savings", "Savings")],
                        max_length=10,
                    ),
                ),
                ("balance", models.FloatField()),
                (
                    "account_number",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="myapp.accountnumber",
                    ),
                ),
            ],
            options={
                "unique_together": {("account_number", "account_type")},
            },
        ),
    ]
