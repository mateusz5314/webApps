from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'table', views.TableViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'task', views.TaskViewSet)

urlpatterns = [
    path('root/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', views.home, name="home"),
]
