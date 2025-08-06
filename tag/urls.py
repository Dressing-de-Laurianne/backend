from django.urls import path

from tag import views

urlpatterns = [
    path("tags/", views.TagList.as_view()),
    path("tags/<int:pk>/", views.TagDetail.as_view()),
]
