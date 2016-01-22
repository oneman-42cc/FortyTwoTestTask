from django.forms import ModelForm
from django.contrib.admin.widgets import AdminDateWidget
from hello.models import Profile
from hello.widgets import ThumbnailFileInput


class ProfileModelForm(ModelForm):

    class Meta:
        model = Profile
        fields = "__all__"
        widgets = {
            "birthday": AdminDateWidget,
            "photo": ThumbnailFileInput,
        }
