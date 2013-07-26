# -*- coding: utf-8 -*-
from django import template
from ishuqian.utils.sina import get_authorize_url

register = template.Library()

@register.tag(name='auth_url')
def auth_url(parser, token):
    try:
        tag_name, site = token.split_contents()
    except ValueError:
        msg = '%r tag requires a site name' % token.split_contents()[0]
        raise template.TemplateSyntaxError(msg)
    return AuthUrlNode(site)

class AuthUrlNode(template.Node):
    def __init__(self, site):
        self.site = site

    def render(self, context):
        if self.site == 'sina':
            return get_authorize_url()
        else:
            return self.site