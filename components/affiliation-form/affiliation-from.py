from django_components import Component, register
from typing import Optional, List
from service.models import Clinic, Doctor


@register('affiliation-form')
class AffiliationForm(Component):
    template_name = 'template.html'


    def get_context_data(self, clinic: Clinic, doctors: Optional[List[Doctor]] = None, doctor: Optional[Doctor] = None):
        return {
            'clinic': clinic,
            'doctors': doctors if doctors else [],
            'doctor': doctor,
        }
    

    class Media:
        js = 'script.js'
