from django_components import Component, register
from service.models import Doctor


@register('doctor-card')
class DoctorCard(Component):
    template_name='template.html'

    
    def get_context_data(self, doctor: Doctor):
        return {
            'doctor': doctor,
        }


    class Media:
        js = 'script.js'