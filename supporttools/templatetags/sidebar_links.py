# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from django import template
from django.template.loader_tags import IncludeNode

register = template.Library()


@register.tag("sidebar_links")
def do_sidebar_links(parser, token):
    custom_template = "supporttools/custom_sidebar_links.html"
    default_template = "supporttools/default_sidelinks.html"
    try:
        template.loader.get_template(custom_template)
        return IncludeNode(parser.compile_filter(
            "'{}'".format(custom_template)))
    except template.TemplateDoesNotExist:
        return IncludeNode(parser.compile_filter(
            "'{}'".format(default_template)))
