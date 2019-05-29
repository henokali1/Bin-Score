from django.urls import path
from . import views


urlpatterns = [
    path('scoreboard/', views.scoreboard),
    path('counter/', views.counter),
    path('register/', views.reg),
    path('bin_stat/', views.bin_stat),
    path('get_all_ids/', views.get_all_ids),
    path('post_score/<int:score>/', views.post_score),
    path('start_cntr/<str:std_id>/', views.start_cntr),
    path('post_bin_stat/<int:bin1>/<int:bin2>/<int:bin3>/', views.post_bin_stat),
]