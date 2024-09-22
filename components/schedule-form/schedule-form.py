from django_components import Component, register
from typing import List
from service.models import Patient, Procedure


@register('schedule-form')
class ScheduleForm(Component):
    template_name = 'template.html'


    def get_context_data(self, patient: Patient, procedures: List[Procedure]):
        return {
            'patient': patient,
            'procedures': procedures,
        }
    

    class Media:
        js = 'script.js'
