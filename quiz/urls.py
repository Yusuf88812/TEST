from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.home, name='home'),
    path('subject/<slug:subject_slug>/', views.subject_detail, name='subject_detail'),
    path('module/<int:module_id>/start/', views.take_test, name='take_test'),
    path('result/<int:attempt_id>/', views.test_result, name='test_result'),
    path('result/<int:attempt_id>/detail/', views.test_result_detail, name='test_result_detail'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('profile/', views.profile, name='profile'),
    path('certificate/<int:attempt_id>/', views.certificate, name='certificate'),
]
