from django.urls import path, re_path

from tag_read import views

urlpatterns = [
    path("tag_read/", views.TagReadList.as_view()),
    path("tag_read/<int:pk>/", views.TagReadDetail.as_view()),
    re_path(r"^tag_wait/(?P<type>hanger|item)/(?P<id>\d+)/$", views.tag_wait),
]
