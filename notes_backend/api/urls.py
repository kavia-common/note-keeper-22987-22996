from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import health, NoteViewSet

router = DefaultRouter()
# Ocean Professional naming: concise, clear, version-neutral base for internal app routing.
router.register(r'notes', NoteViewSet, basename='notes')

urlpatterns = [
    path('health/', health, name='Health'),
    path('', include(router.urls)),
]
