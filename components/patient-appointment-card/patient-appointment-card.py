from django_components import Component, register
from service.models import Appointment


@register('patient-appointment-card')
class PatientAppointmentCard(Component):
    template_name = 'template.html'


    def get_context_data(self, appointment: Appointment):
        return {
            'appointment': appointment,
        }


    class Media:
        js = 'script.js'