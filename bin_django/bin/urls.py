from django.urls import path
from . import views


urlpatterns = [
    path('scoreboard/', views.scoreboard),
    path('counter/', views.counter),
    path('pd/<str:d>/', views.post_data),
    path('t/', views.t),
    path('bin_stat/', views.bin_stat),
    path('start_cntr/<str:std_id>/', views.start_cntr),
    path('post_score/<int:score>/', views.post_score),
]