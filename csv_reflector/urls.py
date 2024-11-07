from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.csv_upload_view, name='csv_upload'),
]
