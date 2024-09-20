from django_components import Component, register


@register('add-patient-form')
class AddPatientForm(Component):
    template_name = 'template.html'


    class Media:
        js = 'script.js'