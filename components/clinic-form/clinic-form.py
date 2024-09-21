from django_components import Component, register
from typing import Optional
from service.models import Clinic


@register('clinic-form')
class ClinicForm(Component):
    template_name = 'template.html'


    def get_context_data(self, clinic: Optional[Clinic] = None):
        return {
            'clinic': clinic,
        }


    class Media:
        js = 'script.js'