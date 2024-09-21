from django_components import Component, register
from typing import Optional
from service.models import Doctor


@register('doctor-form')
class DoctorForm(Component):
    template_name = 'template.html'


    def get_context_data(self, doctor: Optional[Doctor] = None):
        return {
            'doctor': doctor,
        }


    class Media:
        js = 'script.js'