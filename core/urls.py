from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, CompanyViewSet

router = DefaultRouter()
router.register(r'services', ServiceViewSet)
router.register(r'companies', CompanyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
