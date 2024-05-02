from django.db import models
import uuid
from django.utils import timezone


class UuidMixin(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class TimestampMixin(models.Model):
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def deleted(self):
        return super().get_queryset().filter(is_deleted=True)


class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(default=False)

    def delete(self, force_delete=False, **kwargs):
        if force_delete:
            return super().delete(**kwargs)
        if not self.is_deleted:
            self.is_deleted = True
            self.save(update_fields=["is_deleted"])
        return self.is_deleted

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True


