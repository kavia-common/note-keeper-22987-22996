from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("public_id", "title", "created_at", "updated_at", "deleted_at")
    list_filter = ("deleted_at", "created_at", "updated_at")
    search_fields = ("title", "content")
    readonly_fields = ("public_id", "created_at", "updated_at")

