from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

# URL configuration for the store app
'''urlpatterns = [
    path("products/", views.product_list, name="product-list"),
    path("products/<int:id>/", views.product_detail, name="product-detail"),
    path("collections/<int:id>/", views.collection_list, name="collection-list"),
    path("collections/<int:pk>/", views.collection_detail, name="collection-detail"),
]'''

# Routers
router = DefaultRouter()
router.register(r"products", views.ProductViewSet)
router.register(r"collections", views.CollectionViewSet)
router.register(r"admin/products", views.AdminProductViewSet, basename="admin-products")
urlpatterns = router.urls

