from rest_framework import routers

from event_router.views import EventRouterViewSet

# router = routers.SimpleRouter(trailing_slash=False)
router = routers.DefaultRouter()
router.register(r"", EventRouterViewSet, base_name="event-router")

urlpatterns = router.urls
