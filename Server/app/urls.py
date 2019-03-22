from django.urls import path
from app import views

urlpatterns = [
    path('', views.Index),
    path('process', views.Process),
	path('process/<int:meetingNumber>', views.REST_Process),
	path('database', views.Database),
]
