from django.urls import path
from hanger import views

urlpatterns = [
    path('hangers/', views.HangerList.as_view()),
    path('hangers/<int:pk>/', views.HangerDetail.as_view()),
]