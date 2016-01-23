from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class ThumbnailFileInput(ClearableFileInput):

    """A widget for inputs of image field. Present thumbnail of
        uploaded image.
    """

    class Media:
        js = ("js/thumbnailfileinput.widget.js",)
        css = {
            "all": ("css/thumbnailfileinput.widget.css",)
        }

    def render(self, name, value, attrs=None):

        if not value.instance.photo_exist_onserver():
            value = ""

        context = {
            "name": name,
            "value": value,
            "required": self.is_required,
        }

        return mark_safe(render_to_string(
            "hello/widgets/thumbnail_fileinput.html",
            context,
        ))
