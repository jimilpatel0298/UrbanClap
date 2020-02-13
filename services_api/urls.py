from django.urls import path, include
from rest_framework.routers import DefaultRouter
from services_api import views

router = DefaultRouter()
router.register('services', views.ListServices)
router.register('requests', views.MakeServiceRequest)

router1 = DefaultRouter()
router1.register('services', views.MakeService)
router1.register('requests', views.ListOfRequestsToProvider)

urlpatterns = [
    path('consumer/', include(router.urls)),
    path('provider/', include(router1.urls)),
]
