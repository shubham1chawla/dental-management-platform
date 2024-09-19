from django_components import Component, register


@register('page-header')
class PageHeader(Component):
    template_name='template.html'
