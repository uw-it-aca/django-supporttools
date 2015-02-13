from django import template

register = template.Library()


# From https://djangosnippets.org/snippets/2058/
# Previous method started failing with Django 1.7
class IncludeNode(template.Node):
    def __init__(self, template_name):
        self.template_name = template_name

    def render(self, context):
        # Loading the template and rendering it
        included_template = template.loader.get_template(
                                self.template_name).render(context)
        return included_template


@register.tag("sidebar_links")
def do_sidebar_links(parser, token):
    # XXX - should this come from/be overrideable by settings?
    custom_template = "supporttools/custom_sidebar_links.html"
    default_template = "supporttools/default_sidelinks.html"
    try:
        template.loader.get_template(custom_template)
        return IncludeNode(custom_template)
    except template.TemplateDoesNotExist:
        return IncludeNode(default_template)
