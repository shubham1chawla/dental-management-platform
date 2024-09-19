from django_components import Component, register
from service.models import Clinic


@register('clinic-card')
class ClinicCard(Component):
    template_name='template.html'

    
    def get_context_data(self, clinic: Clinic):
        return {
            'clinic': clinic,
        }


    class Media:
        js = 'script.js'