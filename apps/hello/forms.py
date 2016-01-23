from django.forms import ModelForm, ValidationError
from django.contrib.admin.widgets import AdminDateWidget
from hello.models import Profile
from hello.widgets import ThumbnailFileInput


class ProfileModelForm(ModelForm):

    """A form for edit objects of Profile."""

    class Meta:
        model = Profile
        fields = "__all__"
        widgets = {
            "birthday": AdminDateWidget,
            "photo": ThumbnailFileInput,
        }

    def clean_photo(self):

        """Validate a photo field."""

        photo_ = self.cleaned_data["photo"]

        # If there is record about photo in profile, we need to check or this
        # file exist on server.
        if photo_ and not self.instance.photo_exist_onserver():
            # If there is not file on server, ask user upload it.
            raise ValidationError("This field is required.")

        # Always return the cleaned data, whether you have changed it or
        # not.
        return photo_
