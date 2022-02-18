from django.urls import path

from rest_framework import routers
from slackbot import views

urlpatterns = [
    path('test/', views.Test.as_view(), name='test'),
]

router = routers.SimpleRouter()
urlpatterns += router.urls
