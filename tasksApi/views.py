from datetime import datetime

import django.db.models
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
import json

from .serializers import TableSerializer, UserSerializer, TaskSerializer, UserSerializerShort, ListSerializer
from .models import Table, User, Task, List


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
        try:
            uname = data["username"]
            passwd = data["password"]
            user = authenticate(username=uname, password=passwd)
            responseData = {"error": "None", "status": "Authentication failed"}
            if user is not None:
                responseData["status"] = "Authenticated"
                logged = login(request=request, user=user)
            return Response(data=responseData, status=status.HTTP_200_OK)
        except KeyError:
            responseData = {"error": "Incorrect key. Expected keys: username, password", "status": "Authentication "
                                                                                                   "failed"}
            return Response(data=responseData, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def logout(self, request, *args, **kwargs):
        logout(request)
        responseData = {"error": "None", "status": "Logged out"}
        return Response(data=responseData, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def loginStatus(self, request, *args, **kwargs):
        authStatus = request.user.is_authenticated
        responseData = {"error": "None", "status": "Logged out", "uid": -1}
        if authStatus:
            responseData["status"] = f"Active account: {request.user}"
            responseData["uid"] = request.user.id
        else:
            responseData["status"] = f"Active account: None"

        return Response(data=responseData, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def createAccount(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(request.data["password"])
        now = datetime.now()
        user.date_joined = now.strftime("%Y-%m-%d %H:%M:%S")
        user.save()
        responseData = {"error": "None", "status": "success"}
        return Response(data=responseData, status=status.HTTP_200_OK)


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by('id')
    serializer_class = TableSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Table.objects.filter(Q(owner=self.request.user) | Q(access=self.request.user)).distinct()
        else:
            return Table.objects.filter(Q(owner=-1)).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListViewSet(viewsets.ModelViewSet):
    queryset = List.objects.all().order_by('id')
    serializer_class = ListSerializer

    @action(detail=True, methods=['GET'])
    def getLists(self, request, *args, **kwargs):
        tableId = kwargs["pk"]
        error = "None"
        try:
            tableDetails = Table.objects.get(id=tableId)
        except Table.DoesNotExist:
            tableDetails = None
            error = "Table does not exist"
        if tableDetails:
            if request.user == tableDetails.owner or request.user in tableDetails.access.all():
                qs = List.objects.filter(Q(table=tableId))
            else:
                qs = []
        else:
            qs = []
        responseData = {"error": error, "lists": [dict(id=record.id, name=record.name) for record in qs]}
        return Response(data=responseData, status=status.HTTP_200_OK)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('id')
    serializer_class = TaskSerializer

    @action(detail=True, methods=['GET'])
    def getTasks(self, request, *args, **kwargs):
        listId = kwargs["pk"]
        qs = Task.objects.filter(Q(list=listId))
        error = "None"
        if not qs:
            error = "List does not exist"

        responseData = {"error": error, "tasks": [dict(id=record.id, name=record.name,
                                                       description=record.description,
                                                       assigne=record.assignee.id if record.assignee else -1,
                                                       list=record.list.id if record.list else -1, status=record.status)
                                                  for record in qs]}
        return Response(data=responseData, status=status.HTTP_200_OK)


def home(request):
    return render(request, "index.html")
