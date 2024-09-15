# Generated by Django 5.1.1 on 2024-09-15 07:29

import django.db.models.deletion
import phonenumber_field.modelfields
import service.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_address_remove_clinic_city_remove_clinic_state_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('dob', models.DateField()),
                ('ssn', models.IntegerField(validators=[service.models.validate_ssn])),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='service.address')),
            ],
        ),
    ]