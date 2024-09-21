from django_components import Component, register
from typing import Optional
from service.models import Patient


@register('patient-form')
class PatientForm(Component):
    template_name = 'template.html'


    def get_context_data(self, patient: Optional[Patient] = None):
        return {
            'patient': patient,
        }


    class Media:
        js = 'script.js'