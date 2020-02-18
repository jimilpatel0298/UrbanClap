from django.urls import path, include
from rest_framework.routers import DefaultRouter
from services_api import views

router = DefaultRouter()
router.register('services', views.ListServices)
router.register('requests', views.MakeServiceRequest, base_name='request-list')
router.register('comment', views.CreateComment)

router1 = DefaultRouter()
router1.register('services', views.MakeService, base_name='service-list')
router1.register('requests', views.ListOfRequestsToProvider, base_name='request-list')
router1.register('comment', views.CreateComment)


urlpatterns = [
    path('consumer/', include(router.urls)),
    path('provider/', include(router1.urls)),
    path('comments/<int:pk>/', views.ViewComments.as_view(), name="comment_views")
]
