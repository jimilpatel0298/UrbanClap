from django.urls import path, include
from rest_framework.routers import DefaultRouter
from services_api import views as v

router = DefaultRouter()
router.register('services', v.ListServices)
router.register('request', v.MakeServiceRequest, base_name='request-list')

router1 = DefaultRouter()
router1.register('', v.MakeService, base_name='service-list')
router1.register('comment', v.CreateComment)

urlpatterns = [
    path('consumer/', include(router.urls)),
    path('provider/', include(router1.urls)),
]
