from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class ThumbnailFileInput(ClearableFileInput):

    class Media:
        js = ("js/thumbnailfileinput.widget.js",)
        css = {
            "all": ("css/thumbnailfileinput.widget.css",)
        }

    def render(self, name, value, attrs=None):

        context = {
            "name": name,
            "value": value,
            "required": self.is_required,
        }

        return mark_safe(render_to_string(
            "hello/widgets/thumbnail_fileinput.html",
            context,
        ))
