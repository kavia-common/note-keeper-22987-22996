from django.db import models
from django.utils import timezone
import uuid


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides created_at and updated_at fields for
    consistent temporal tracking across entities.
    """
    created_at = models.DateTimeField(default=timezone.now, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Abstract base model providing soft-delete capability via deleted_at.
    """
    deleted_at = models.DateTimeField(null=True, blank=True, default=None, db_index=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """
        Override hard delete with soft delete for safer removals.
        """
        self.deleted_at = timezone.now()
        self.save(update_fields=["deleted_at", "updated_at"] if hasattr(self, "updated_at") else ["deleted_at"])

    def hard_delete(self, using=None, keep_parents=False):
        """
        Perform a real database delete.
        """
        return super().delete(using=using, keep_parents=keep_parents)


class NoteQuerySet(models.QuerySet):
    """
    QuerySet with helpers to filter out deleted notes.
    """
    def alive(self):
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        return self.exclude(deleted_at__isnull=True)


class NoteManager(models.Manager):
    """
    Manager exposing default alive() behavior.
    """
    def get_queryset(self):
        return NoteQuerySet(self.model, using=self._db).alive()

    # PUBLIC_INTERFACE
    def all_with_deleted(self):
        """Return queryset including soft-deleted records."""
        return NoteQuerySet(self.model, using=self._db).all()


class Note(TimeStampedModel, SoftDeleteModel):
    """
    Note entity representing a simple text note with optional title.
    Uses a human-safe public_id for API exposure (Ocean Professional style).
    """
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    title = models.CharField(max_length=255, blank=True, default="")
    content = models.TextAreaField = models.TextField(blank=True, default="")
    # In future we can add user foreign key for multi-user support.

    objects = NoteManager()

    class Meta:
        db_table = "notes"
        ordering = ["-updated_at", "-created_at"]
        indexes = [
            models.Index(fields=["public_id"]),
            models.Index(fields=["updated_at"]),
        ]

    def __str__(self) -> str:
        return f"Note<{self.public_id}> {self.title[:50] if self.title else '(untitled)'}"
