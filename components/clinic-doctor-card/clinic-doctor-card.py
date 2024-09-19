from django_components import Component, register
from service.models import Doctor, Clinic


@register('clinic-doctor-card')
class ClinicDoctorCard(Component):
    template_name='template.html'

    
    def get_context_data(self, doctor: Doctor, clinic: Clinic):
        return {
            'doctor': doctor,
            'clinic': clinic,
        }


    class Media:
        js = 'script.js'