from django.urls import path, include
from rest_framework.routers import DefaultRouter
from services_api import views as v


router = DefaultRouter()
router.register('services', v.ListServices)
router.register('request', v.MakeServiceRequest)


router1 = DefaultRouter()
router1.register('', v.MakeService)

urlpatterns = [
    path('consumer/', include(router.urls)),
    path('provider/', include(router1.urls)),
]