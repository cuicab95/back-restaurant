from rest_framework import routers
from . import views

app_name = "business"
router = routers.SimpleRouter()
router.register("restaurant", views.RestaurantViewSet)
urlpatterns = router.urls
