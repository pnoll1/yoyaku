from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from .models import reservation

Group.objects.get_or_create(name="callers")
content_type = ContentType.objects.get_for_model(reservation)
permission = Permission.objects.create(
    codename='can_accept_calls',
    name='Accept Call',
    content_type=content_type,
)

# allow users to edit their reservations
