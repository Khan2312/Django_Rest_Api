from django.urls import path, include
from rest_framework.routers import DefaultRouter

from myapi import views

router = DefaultRouter()
router.register('content', views.ContentViewSet)

app_name = 'content'

urlpatterns = [
    path('', include(router.urls))
]
