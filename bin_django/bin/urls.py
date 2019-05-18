from django.urls import path
from . import views


urlpatterns = [
    path('score_bord/', views.score_bord),
    path('counter/', views.counter),
    path('pd/<str:d>/', views.post_data),
    path('t/', views.t),
]