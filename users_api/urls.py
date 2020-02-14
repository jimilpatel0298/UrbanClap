from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users_api import views

router = DefaultRouter()
router.register('users', views.UserProfileViewSet)
router.register('update', views.UserUpdateView)
router.register('users/<int:pk>/update', views.UserUpdateView)
router.register('password', views.ChangePasswordView)

urlpatterns = [
    path('', include(router.urls)),
]