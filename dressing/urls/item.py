from django.urls import path

from dressing import views

urlpatterns = [
    path("items/", views.ItemList.as_view()),
    path("items/<int:pk>/", views.ItemDetail.as_view()),
]
