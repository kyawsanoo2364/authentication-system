from django.urls import path
from .views import GoogleApiView

urlpatterns = [path("google/", GoogleApiView.as_view(), name="auth-google")]
