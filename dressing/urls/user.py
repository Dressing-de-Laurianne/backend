from rest_framework import routers

from dressing import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)

urlpatterns = router.urls
