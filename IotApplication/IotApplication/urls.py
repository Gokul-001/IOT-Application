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
    
    #Creates new device [post] | list all devices [get]
    path("api/devices/",views.DevicePOSTGETOperations.as_view()),

    #Retrieve device properties [get] | DElete a device [Delete]
    path("api/devices/<uuid:device_id>/",views.DeviceGETDELETEOperations.as_view()),
    
    #Retrieve a devices with readings [get]
    path("api/devices/<uuid:device_id>/readings/<str:parameter>/",views.DeviceReadingsView.as_view(),name="Retrieve the Device Readings"),
    
    #Plot the readings of a device [get]
    path("device-graph/<uuid:device_id>/",views.plot_reading,name="Graph of a Device readings"),
]
