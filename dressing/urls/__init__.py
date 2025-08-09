from django.urls import include, path

app_name = "dressing"

urlpatterns = [
    path("", include("dressing.urls.user")),
    path("", include("dressing.urls.item")),
    path("", include("dressing.urls.hanger")),
    path("", include("dressing.urls.outfit")),
    path("", include("dressing.urls.order")),
    path("", include("dressing.urls.tag")),
    path("", include("dressing.urls.tag_read")),
]
