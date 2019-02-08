from django.contrib import admin
from django.urls import path

from rest_framework import routers
from graphene_django.views import GraphQLView

from django_pivot.tests.test_project.testapp import views
from django_pivot.tests.test_project.testapp import viewsets

router = routers.DefaultRouter()
router.register('meteo', viewsets.MeteoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('provider/', views.ProviderListView.as_view(), name='provider-list'),
    path('provider/filter/', views.ProviderFilterView.as_view(), name='provider-filter'),
    path('meteo/', views.MeteoListView.as_view(), name='meteo-list'),
    path('meteo/filter/', views.MeteoFilterView.as_view(), name='meteo-filter'),
    path('graphql/', GraphQLView.as_view(graphiql=True), name="graphql"),
] + router.urls
