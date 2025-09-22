from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Note
from .serializers import NoteSerializer


@api_view(['GET'])
def health(request):
    """
    Ocean Professional Health Endpoint.

    Returns a simple status message to indicate the service is operational.
    """
    return Response({"message": "Server is up!"})


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination with Ocean Professional defaults for consistent API ergonomics.
    """
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 200


class NoteViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    CRUD interface for Notes.

    Tags: notes
    """
    serializer_class = NoteSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ["title", "content"]
    ordering_fields = ["created_at", "updated_at", "title"]

    def get_queryset(self):
        """
        Limit default queryset to alive notes only; soft-deleted notes are excluded.
        """
        return Note.objects.all()

    @swagger_auto_schema(
        operation_id="notes_list",
        operation_summary="List notes",
        operation_description="Retrieve a paginated list of notes. Soft-deleted notes are excluded.",
        tags=["notes"],
        manual_parameters=[
            openapi.Parameter("search", openapi.IN_QUERY, description="Search in title or content", type=openapi.TYPE_STRING),
            openapi.Parameter("ordering", openapi.IN_QUERY, description="Comma-separated fields to order by", type=openapi.TYPE_STRING),
            openapi.Parameter("page", openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter("page_size", openapi.IN_QUERY, description="Items per page (max 200)", type=openapi.TYPE_INTEGER),
        ],
        responses={200: NoteSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="notes_create",
        operation_summary="Create a note",
        operation_description="Create a new note with optional title and content.",
        tags=["notes"],
        request_body=NoteSerializer,
        responses={201: NoteSerializer, 400: "Validation error"},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="notes_retrieve",
        operation_summary="Get a note",
        operation_description="Retrieve a note by its public UUID.",
        tags=["notes"],
        responses={200: NoteSerializer, 404: "Not found"},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="notes_update",
        operation_summary="Update a note",
        operation_description="Replace all fields of a note identified by its public UUID.",
        tags=["notes"],
        request_body=NoteSerializer,
        responses={200: NoteSerializer, 400: "Validation error", 404: "Not found"},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="notes_partial_update",
        operation_summary="Partially update a note",
        operation_description="Update specific fields of a note identified by its public UUID.",
        tags=["notes"],
        request_body=NoteSerializer,
        responses={200: NoteSerializer, 400: "Validation error", 404: "Not found"},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_id="notes_delete",
        operation_summary="Delete a note",
        operation_description="Soft delete a note by setting deleted_at. Use admin for hard delete if necessary.",
        tags=["notes"],
        responses={204: "Deleted", 404: "Not found"},
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
