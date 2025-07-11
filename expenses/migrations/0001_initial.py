# Generated by Django 5.2.3 on 2025-06-13 18:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('category', models.CharField(choices=[('FOOD', 'Food'), ('TRAVEL', 'Travel'), ('UTILITIES', 'Utilities'), ('MISC', 'Miscellaneous')], db_index=True, max_length=50)),
                ('date', models.DateField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
