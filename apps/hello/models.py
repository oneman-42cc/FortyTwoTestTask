from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    """Model Profile store profile data of user."""

    class Meta:
        app_label = "hello"

    def __unicode__(self):
        return "Profile of %s" % self.email

    email = models.EmailField(null=True)
    first_name = models.CharField(max_length=256, null=True)
    last_name = models.CharField(max_length=256, null=True)
    birthday = models.DateField(blank=True, null=True)

    jabber = models.CharField(max_length=256, blank=True)
    skype = models.CharField(max_length=256, blank=True)

    bio = models.TextField(blank=True)
    contacts_other = models.TextField(blank=True)


class Request(models.Model):

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
