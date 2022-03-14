from django.shortcuts import render
from rest_framework import viewsets

from .serializers import PersonSerializer, TaskSerializer
from .models import Person, Task


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all().order_by('id')
    serializer_class = PersonSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('id')
    serializer_class = TaskSerializer


def home(request):
    return render(request, "index.html")
