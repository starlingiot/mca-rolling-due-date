from django.urls import path
from mca_test_monitor.orders import views

urlpatterns = [
    path("", views.RollingDueDateView.as_view(), name="rolling-due-date"),
    path('<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path("notes", views.NoteView.as_view(), name='note-view'),
]
