from django_components import Component, register


@register('add-clinic-form')
class AddClinicForm(Component):
    template_name = 'template.html'


    class Media:
        js = 'script.js'