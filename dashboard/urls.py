from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('Dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_car_image, name='upload_license_plate'),
]
