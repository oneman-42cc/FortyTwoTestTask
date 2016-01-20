from django.db import models


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
