# Generated by Django 5.0.6 on 2024-07-04 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hhapp', '0005_alter_vacancy_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=10, null=True),
        ),
    ]
