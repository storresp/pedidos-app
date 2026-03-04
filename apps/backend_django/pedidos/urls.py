from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, ProductViewSet, OrderViewSet

router = DefaultRouter()
router.register(r"customers", CustomerViewSet, basename="customers")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("api/", include(router.urls)),
]