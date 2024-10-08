# Generated by Django 5.1.1 on 2024-09-22 23:07

from django.db import migrations


DEFAULT_PROCEDURES = [
    'Cleaning', 
    'Filling', 
    'Root Canal', 
    'Crown', 
    'Teeth Whitening',
]

def add_procedures(apps, _):
    Procedure = apps.get_model('service', 'Procedure')
    for name in DEFAULT_PROCEDURES:
        entity = Procedure(name=name)
        entity.save()


def remove_procedures(apps, _):
    Procedure = apps.get_model('service', 'Procedure')
    for name in DEFAULT_PROCEDURES:
        entity = Procedure.objects.get(name=name)
        entity.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_procedures, remove_procedures),
    ]
