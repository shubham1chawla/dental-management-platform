from django_components import Component, register


@register('navbarlink')
class NavbarLink(Component):
    template_name = 'template.html'

    def get_context_data(self, title: str, href: str, active: bool = False):
        return {
            'title': title,
            'href': href,
            'active': 'active' if active else '',
        }
