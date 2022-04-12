from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
import json

from .serializers import TableSerializer, UserSerializer
from .models import Table, User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

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


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by('id')
    serializer_class = TableSerializer

    def get_queryset(self):
        return Table.objects.filter(Q(owner=self.request.user) | Q(access=self.request.user)).distinct()


def home(request):
    return render(request, "index.html")
