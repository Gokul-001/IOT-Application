"""
URL configuration for IotApplication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from DeviceApp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    #Creates new device [post] 
    path("api/devices/",views.DeviceCreateView.as_view(),name="Device List"),
    #list all devices [get]
    path("api/devices-all/",views.DeviceListAllView.as_view(),name="Device Retrieve All"),
    #delete a device [ delete ]
    path("api/device-delete/<uuid:device_id>/",views.DeviceDeleteView.as_view(),name="Device Delete"),
    #Retrieve device properties [get]
    path("api/device-get/<uuid:device_id>/",views.DeviceRetrieveView.as_view(),name="Device Retrieve"),
    #Retrieve a devices with readings [get]
    path("api/devices-readings/<uuid:device_id>/readings/<str:parameter>/",views.DeviceReadingsView.as_view(),name="Device Readings"),
    #Plot the readings of a device [get]
    path("device-graph/<uuid:device_id>/",views.plot_reading,name="Device graph"),
]
