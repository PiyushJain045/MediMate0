from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home_page'),
    path('Diagnosis', views.Diagonisis.as_view(), name='home'),
    path('Questions', views.Questions.as_view(), name='questions'),
    path('Skin Disease', views.SkinDisease.as_view(), name='skin_disease'),
    path('Nearby Doctors', views.NearbyDoctor.as_view(), name='nearby_doctors'), 
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('Calendar', views.CalendarView.as_view(), name='calendar'),
]
