from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import connection
from hello.models import Entry


@receiver(post_save)
def any_model_post_save(sender, *args, **kwargs):

    instance = kwargs.get("instance")

    # Do not create entry for itself.
    if isinstance(instance, Entry):
        return

    # Check or exist table for entries.
    if "hello_entry" in connection.introspection.table_names():
        Entry.objects.create(
            content_object=instance,
            event="creation" if kwargs.get("created") else "editing",
        )


@receiver(post_delete)
def any_model_post_delete(sender, *args, **kwargs):

    instance = kwargs.get("instance")

    # Do not create entry for itself.
    if isinstance(instance, Entry):
        return

    # Check or exist table for entries.
    if "hello_entry" in connection.introspection.table_names():
        Entry.objects.create(
            content_object=instance,
            event="deletion",
        )
