import json
import os.path
import tempfile
from PIL import Image
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


class Profile(models.Model):

    """Model Profile store profile data of user."""

    email = models.EmailField(null=True)
    first_name = models.CharField(max_length=256, null=True)
    last_name = models.CharField(max_length=256, null=True)
    birthday = models.DateField(blank=True, null=True)

    jabber = models.CharField(max_length=256, blank=True)
    skype = models.CharField(max_length=256, blank=True)

    bio = models.TextField(blank=True)
    contacts_other = models.TextField(blank=True)

    photo = models.ImageField(upload_to="profile/photo", null=True)

    class Meta:
        app_label = "hello"

    def __unicode__(self):
        return "Profile of %s" % self.email

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        if not self.photo or not self.photo_exist_onserver():
            return

        maxsize = (200, 200)

        image_ = Image.open(self.photo.path)
        image_.thumbnail(maxsize, Image.ANTIALIAS)

        image_.save(self.photo.path)

    def photo_exist_onserver(self):

        """Method to check or exist photo on the server."""

        if not self.photo:
            return False

        if os.path.isfile(self.photo.path):
            return True

        return False

    def set_temporary_photo(self):

        """This method set a temporary image as a photo of profile. Use this
            method in general in tests.
        """

        image_ = self.get_temporary_photo()

        self.photo = image_.name
        self.save()

    def get_temporary_photo(self, pil=False):

        """This method generates a temporary image, which load from
            fixtures. Use this method in general in tests.
            A temporary image has dimensions of 512x512px and extension
            of png.
        """

        # Set path to fixture with photo.
        fixture = os.path.dirname(__file__) + "/fixtures/temporary_photo.json"
        # Load and decode.
        photo = json.load(file(fixture)).get("photo", False)\
            .strip().decode("base64")

        # Create a temporary file and write to is data from fixtures.
        with tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False,
            dir=settings.MEDIA_ROOT,
        ) as png:
            png.write(photo)
            png.seek(0)
            image_ = SimpleUploadedFile(
                png.name,
                png.read(),
                content_type="image/png",
            )

            return Image.open(image_) if pil else image_


class Request(models.Model):

    """Model Request use to store all http requests."""

    class Meta:
        app_label = "hello"
        ordering = ["-date"]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    url = models.URLField()
    date = models.DateTimeField(auto_now=True, auto_now_add=True)
