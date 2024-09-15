# Generated by Django 5.1.1 on 2024-09-15 06:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_auto_20240915_0528'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorClinicAffiliation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clinic_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.doctor')),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service.clinic')),
            ],
            options={
                'unique_together': {('clinic_id', 'doctor_id')},
            },
        ),
    ]
