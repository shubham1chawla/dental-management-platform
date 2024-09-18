from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', view=views.get_dashboard, name='Dashboard Page'),
]
