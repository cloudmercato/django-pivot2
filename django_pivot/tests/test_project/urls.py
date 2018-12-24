from django.contrib import admin
from django.urls import path
from django_pivot.tests.test_project.testapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('provider/', views.ProviderListView.as_view(), name='provider-list'),
    path('provider/filter/', views.ProviderFilterView.as_view(), name='provider-filter'),
    path('meteo/', views.MeteoListView.as_view(), name='meteo-list'),
    path('meteo/filter/', views.MeteoFilterView.as_view(), name='meteo-filter'),
]
