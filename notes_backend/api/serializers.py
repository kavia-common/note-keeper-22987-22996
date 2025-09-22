from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for Note model with clean, Ocean Professional-style documentation.
    Exposes 'id' as public_id for a stable external identifier.
    """
    # PUBLIC_INTERFACE
    def to_representation(self, instance):
        """Customize representation to expose 'id' as the public UUID."""
        data = super().to_representation(instance)
        data["id"] = data.pop("public_id")
        return data

    class Meta:
        model = Note
        fields = [
            "public_id",
            "title",
            "content",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["public_id", "created_at", "updated_at"]

    # PUBLIC_INTERFACE
    def validate_title(self, value: str) -> str:
        """Ensure title isn't purely whitespace."""
        if value and not value.strip():
            return ""
        return value

    # PUBLIC_INTERFACE
    def validate(self, attrs):
        """Enforce at least one of title or content is provided."""
        title = attrs.get("title", "")
        content = attrs.get("content", "")
        if not (title.strip() or content.strip()):
            raise serializers.ValidationError("A note requires at least a title or content.")
        return attrs
