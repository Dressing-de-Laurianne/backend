from django.urls import path
from outfit import views

urlpatterns = [
    path('outfits/', views.OutfitList.as_view()),
    path('outfits/<int:pk>/', views.OutfitDetail.as_view()),
]