# Generated by Django 5.0.6 on 2024-07-04 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hhapp', '0002_vacancy_alter_hh_info_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HH_info',
        ),
        migrations.AlterModelOptions(
            name='vacancy',
            options={'verbose_name': 'Vacancy', 'verbose_name_plural': 'Vacancs'},
        ),
        migrations.AddField(
            model_name='vacancy',
            name='salary',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]