# Generated by Django 4.0.4 on 2022-04-23 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('role', models.CharField(max_length=50)),
                ('slot_date', models.DateField()),
                ('from_time', models.TimeField()),
                ('to_time', models.TimeField()),
            ],
            options={
                'db_table': 'UserSlot',
            },
        ),
    ]
