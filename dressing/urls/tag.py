from django.urls import path

from dressing import views

urlpatterns = [
    path("tags/", views.TagList.as_view()),
    path("tags/<int:pk>/", views.TagDetail.as_view()),
]
