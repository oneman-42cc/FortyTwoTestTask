# flake8: noqa


import hello.signals
from south.models import MigrationHistory

stupied_migrations = MigrationHistory.objects.filter(
    migration__in=["0003_auto__del_field_request_read", "0004_auto__add_field_profile_photo"],
)

import sys
print >> sys.stderr, stupied_migrations
