from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class GithubWebhookAPIView(APIView):
    """
    API for handling events from Github
    """
    def post(self, request, *args, **kwargs):
        print(request.data)
        return Response(data="success", status=status.HTTP_200_OK)
