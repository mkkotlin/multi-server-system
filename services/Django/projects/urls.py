from rest_framework.routers import DefaultRouter
from projects.views import ProjectViewSet

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="projects")

urlpatterns = router.urls