from django.urls import path

from user_profile import views

urlpatterns = [
    path('', views.ProfileSettingsView.as_view(), name='profile_settings'),
]
