from django_components import Component, register


@register('add-doctor-form')
class AddDoctorForm(Component):
    template_name = 'template.html'


    class Media:
        js = 'script.js'