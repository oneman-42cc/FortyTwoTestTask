from django.test import TestCase
from django.template import Context, Template, TemplateSyntaxError
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from hello.models import Profile


class EditLinkTagTest(TestCase):

    """Test to check a templte tag - edit_link."""

    def test_to_check_tag(self):

        """Test to check or template tag edit_link renders
            it correct.
        """

        profile_ = Profile.objects.first()
        # Create a little template with tag.
        template_ = Template('{% load hello %}{% edit_link object %}')
        context_ = Context({
            "object": profile_,
        })
        # Get admin edit url.
        type_ = ContentType.objects.get_for_model(profile_.__class__)
        admin_url = reverse(
            "admin:%s_%s_change" % (type_.app_label, type_.model),
            args=(profile_.id,),
        )
        # Render a template.
        rendered = template_.render(context_)

        self.assertIn(admin_url, rendered)

    def test_render_tag_without_object_in_context(self):

        """Test to check whan no pass object to template tag."""

        template_ = Template('{% load hello %}{% edit_link object %}')
        # Create empty context.
        context_ = Context({})

        # Render a template.
        rendered = template_.render(context_)

        self.assertEqual(rendered, "")

    def test_render_tag_without_param_object(self):

        """Test to check a exception whan there is not object param."""

        # Create template with tag, but without object param.
        # Must be exeption.
        with self.assertRaises(TemplateSyntaxError):
            Template('{% load hello %}{% edit_link %}')
