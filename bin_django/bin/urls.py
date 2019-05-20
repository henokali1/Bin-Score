from django.urls import path
from . import views


urlpatterns = [
    path('scoreboard/', views.scoreboard),
    path('counter/', views.counter),
    path('pd/<str:d>/', views.post_data),
    path('t/', views.t),
    path('a/', views.a),
]