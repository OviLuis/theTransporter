import datetime


from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Driver
from .serializers import DriverSerializer


class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all().order_by('-id')
    serializer_class = DriverSerializer

    def create(self, request, *args, **kwargs):
        data = self.request.data

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        data = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        final_status = status.HTTP_200_OK
        return Response(data=data, status=final_status, headers=headers)

    def update(self, request, *args, **kwargs):
        print()
        updated_by = request.user
        data = self.request.data

        serializer = self.get_serializer(self.get_object(), data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        final_status = status.HTTP_200_OK
        return Response(status=final_status, template_name=None, content_type=None)

    def get_object(self):
        return get_object_or_404(Driver, pk=self.kwargs.get('pk'))