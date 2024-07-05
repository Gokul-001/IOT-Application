import base64
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework import serializers,generics
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from django.db import IntegrityError
#from IotApplication.logControl import logger
from .models import Device,TemperatureReadings,HumidityReadings
from .serializers import DeviceSerializer,TemperatureSerializer,HumiditySerializer
import template

# Creates (post)/ List(get) - all the devices
'''
class DeviceListCreateView(generics.ListCreateAPIView):
    queryset=Device.objects.all()
    serializer_class=DeviceSerializer

'''

class DeviceCreateView(APIView):
    def post(self,request,format=None):
        try:
            device_name=request.data.get('deviceName')
            if not device_name:
                return Response(
                    {"Error": "Device name is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            device=Device.objects.filter(deviceName__iexact=device_name).first()
            if device:
                return Response(
                    {
                        "Error":"Device already exists"
                    },status=status.HTTP_409_CONFLICT
                )
            else:
                device=Device(deviceName=device_name)
                device.save()
                serialized_device = DeviceSerializer(device)
                return Response(
                    serialized_device.data,
                    status=status.HTTP_201_CREATED
            )
        except IntegrityError:
            return Response(
                {"Error": "Device creation failed due to integrity constraint"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message":str(e)},status=status.HTTP_400_BAD_REQUEST
            )

class DeviceDeleteView(APIView):
    def delete(self,request,device_id=None,format=None):
        if device_id:
            try:
                device=Device.objects.get(deviceId=device_id)
            except Device.DoesNotExist:
                return Response({
                    "ERROR" : 'Requested device not found',
                    "Status":404
                },
                status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response(
                    {
                        "message":e
                    },status=status.HTTP_404_NOT_FOUND
                )
            device.delete()
            #logger("delete").info("dleted success")
            print("Deleted")
            return Response({
                    "INFO" : 'Requested device is Deleted',
                    "Status":200
                },
                status=status.HTTP_200_OK)
        else:
            return Response({
                    "ERROR" : 'Method error',
                    "Status":405
                },status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
class DeviceRetrieveView(APIView):
    def get(self,request,device_id,format=None):
        try:
            device=Device.objects.get(deviceId=device_id)
        except Device.DoesNotExist:
            return Response({
                "ERROR" : 'Requested device not found',
                "Status":404
            },
            status=status.HTTP_404_NOT_FOUND)
        serializedData=DeviceSerializer(device)
        return Response(serializedData.data,status=status.HTTP_200_OK)

class DeviceListAllView(APIView):
    def get(self,request,format=None):
        try:
            device=Device.objects.all()
            serializedData=DeviceSerializer(device,many=True)
            return Response(serializedData.data,status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response({
                "ERROR" : 'No device found',
                "Status":404
            },
            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
class DeviceReadingsView(APIView):
    def get(self,request,parameter,device_id,format=None):
        start_on=request.query_params.get("start_on")
        end_on=request.query_params.get("end_on")

        try:
            start_time=datetime.strptime(start_on,"%Y-%m-%dT%H:%M:%S")
            end_time=datetime.strptime(end_on,"%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return Response(
                {
                    "Error":"Invaild Date-Time format",
                    "status":400
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if parameter not in ["temperature","humidity"]:
            return Response(
                {
                    "Error":"Invaild parameter",
                    "status":4003
                },
                status=status.HTTP_400_BAD_REQUEST
            )
           
        try:
            device=Device.objects.get(deviceId=device_id)
            if parameter=='temperature':
                readings=TemperatureReadings.objects.filter(
                    device__deviceId=device_id,
                    timestamp__gt=start_time,
                    timestamp__lt=end_time
                )
            else:
                readings=HumidityReadings.objects.filter(
                    device__deviceId=device_id,
                    timestamp__gt=start_time,
                    timestamp__lt=end_time
                )
            if readings and parameter=="temperature":
                serialized_data=TemperatureSerializer(readings,many=True)
            elif readings and parameter=='humidity':
                serialized_data=HumiditySerializer(readings,many=True)

            response_data={
                'Device Name':device.deviceName,
                "Readings":serialized_data.data
            }

            return Response(response_data,status=status.HTTP_200_OK)
        except Device.DoesNotExist:
            return Response({
                "ERROR" : 'No device found',
                "Status":404
            },
            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {
                    "Error":"No data found",
                    "Additional Info":e,
                    "status":404
                },
                status=status.HTTP_404_NOT_FOUND
            )

                        
def plot_reading(request,device_id):
    try:
        device = Device.objects.get(deviceId=device_id)
        temperature_readings = TemperatureReadings.objects.filter(device=device)
        humidity_readings = HumidityReadings.objects.filter(device=device)
    except Device.DoesNotExist:
        return render(request, "error.html", {"error_message": "Device not found"})
    time_graph=[data.timestamp for data in temperature_readings]
    temperature_graph=[data.temp for data in temperature_readings]
    humidity_graph=[data.humid for data in humidity_readings]

    #plotting 
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from io import BytesIO

    title=f"Device {device.deviceName} - Temperature and Humidity Readings"
    fig,ax=plt.subplots(figsize=(10,6))
    ax.set_title(title)
    ax.plot(time_graph,temperature_graph,label="Temperature")
    ax.plot(time_graph,humidity_graph,label="Humidity")
    plt.xlabel("Time")
    plt.ylabel("Readings")
    plt.legend()
    buf=BytesIO()
    plt.savefig(buf,format='png')
    buf.seek(0)
    plt.close()
    graph=base64.b64encode(buf.getvalue()).decode("utf-8")
    return render(request, "graph.html", {"graph": graph})






