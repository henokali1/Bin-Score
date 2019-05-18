from django.urls import path
from . import views


urlpatterns = [
    path('pd/<str:d>/', views.post_data),
    path('t/', views.t),
]