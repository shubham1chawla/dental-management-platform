from django_components import Component, register
from service.models import Patient


@register('patient-card')
class PatientCard(Component):
    template_name = 'template.html'


    def get_context_data(self, patient: Patient):
        return {
            'patient': patient,
        }


    class Media:
        js = 'script.js'