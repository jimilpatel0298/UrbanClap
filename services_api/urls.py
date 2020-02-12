from django.urls import path, include
from rest_framework.routers import DefaultRouter
from services_api import views as v


router = DefaultRouter()
router.register('', v.ListOfRequestsToProvider)
router.register('services/', v.MakeService)

router1 = DefaultRouter()
router1.register('', v.ListOfServices)
router1.register('request/', v.MakeServiceRequest)

urlpatterns = [
    path('provider-dashboard/', include(router.urls)),
    path('consumer-dashboard/', include(router1.urls)),
    path("", include())
]