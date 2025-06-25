from . import views
from django.urls import path

app_name = 'app'

urlpatterns = [
    path('trainer/create-intern/', views.create_intern_view, name='create_intern'),
    path('trainer/interns/', views.trainer_interns_view, name='trainer_interns'),
    path('intern/', views.intern_dashboard, name='intern_dashboard'),
    path('intern/start-test/', views.start_test_view, name='start_test'),
    path('intern/detail/',views.intern_detail,name='intern_detail'),
    path('intern/test/<int:pk>/', views.intern_test_detail, name='intern_test_detail'),
]
