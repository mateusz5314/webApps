from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
import json

from .serializers import TableSerializer, UserSerializer, TaskSerializer, UserSerializerShort
from .models import Table, User, Task


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserSerializer
        else:
            return UserSerializerShort

    @action(detail=False, methods=['POST'])
    def login(self, request, *args, **kwargs):
        data = json.loads(request.body)
        uname = data["login"]
        passwd = data["passwd"]
        user = authenticate(username=uname, password=passwd)
        if user is not None:
            response = Response(data="Authenticated")
            logged = login(request=request, user=user)
        else:
            response = Response(data="Authentication failed")

        return response

    @action(detail=False, methods=['POST'])
    def logout(self, request, *args, **kwargs):
        logout(request)
        response = Response(data="Logged out")
        return response

    @action(detail=False, methods=['GET'])
    def loginStatus(self, request, *args, **kwargs):
        authStatus = request.user.is_authenticated
        if authStatus:
            response = f"Active account: {request.user}"
        else:
            response = f"Active account: None"

        return Response(data=response)

    @action(detail=False, methods=['POST'])
    def createAccount(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(request.data["password"])
        now = datetime.now()
        user.date_joined = now.strftime("%Y-%m-%d %H:%M:%S")
        user.save()
        return Response(data="success", status=status.HTTP_200_OK)


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by('id')
    serializer_class = TableSerializer

    def get_queryset(self):
        return Table.objects.filter(Q(owner=self.request.user) | Q(access=self.request.user)).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('id')
    serializer_class = TaskSerializer

    @action(detail=True, methods=['GET'])
    def getTasks(self, request, *args, **kwargs):
        tableId = kwargs["pk"]
        tableDetails = Table.objects.get(id=tableId)
        print(tableDetails.access.all())
        if request.user == tableDetails.owner or request.user in tableDetails.access.all():
            qs = Task.objects.filter(Q(table=tableId))
        else:
            qs = []
        return Response(data=[dict(name=record.name) for record in qs])


def home(request):
    return render(request, "index.html")
