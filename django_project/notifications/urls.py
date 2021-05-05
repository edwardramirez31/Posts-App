from django.urls import path
from .views import get_notifications, mark_notification
app_name = "notifications"

urlpatterns = [
    path('', get_notifications, name="list"),
    path('mark/<int:pk>/', mark_notification, name="mark")
]