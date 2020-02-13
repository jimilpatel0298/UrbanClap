from django.urls import path, include
from rest_framework.routers import DefaultRouter
from services_api import views as v


router = DefaultRouter()
router.register('provider', v.MakeService)
router.register('consumer', v.ListOfServices)
router.register('consumer/<int:pk>/request', v.MakeServiceRequest, basename='request-detail')

# router1 = DefaultRouter()
# router1.register('', v.ListOfServices)
# router1.register('request/', v.MakeServiceRequest)

urlpatterns = [
    path('dashboard/', include(router.urls)),
]