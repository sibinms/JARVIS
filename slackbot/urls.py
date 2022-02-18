from django.urls import path

from rest_framework import routers
from slackbot import views

urlpatterns = [
    path('github-webhook/', views.GithubWebhookAPIView.as_view(), name='github-webhook'),
]

router = routers.SimpleRouter()
urlpatterns += router.urls
