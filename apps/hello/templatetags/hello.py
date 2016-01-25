from django import template
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

register = template.Library()


class EditLinkTag(template.Node):

    """Renders the link to object admin edit page."""

    def __init__(self, parser, token):

        self.tokens = token.split_contents()

        try:
            self.tokens[1]
        except IndexError:
            raise template.TemplateSyntaxError(
                "Second argument in %r tag must be a instance of object."
                % self.tokens[0]
            )

        if len(self.tokens) == 2:
            self.object_ = parser.compile_filter(self.tokens[1])

    def render(self, context):

        instance = self.object_.resolve(context)

        if not instance:
            raise template.TemplateSyntaxError(
                """Second argument in %r tag must be a instance of object.
                    Pass correct context into template.
                """ % self.tokens[0]
            )

        type_ = ContentType.objects.get_for_model(instance.__class__)

        admin_url = reverse(
            "admin:%s_%s_change" % (type_.app_label, type_.model),
            args=(instance.id,),
        )

        return """<a href="%s">Edit (admin)</a>""" % admin_url


@register.tag
def edit_link(parser, token):

    """
        Renders the link to object admin edit page.
        Syntax:

            >>> {% edit_link object %}

    """
    return EditLinkTag(parser, token)
