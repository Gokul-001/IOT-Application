from django.db import models
import uuid
# Create your models here.
class Device(models.Model):
    deviceId=models.UUIDField(max_length=10,default=uuid.uuid4,primary_key=True,unique=True,editable=False)
    deviceName=models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"uniqueID: {self.deviceId}\ndeviceName:{self.deviceName}"

class TemperatureReadings(models.Model):
    id = models.AutoField(primary_key=True) 
    device=models.ForeignKey(Device,on_delete=models.CASCADE)
    temp=models.FloatField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Temperature: {self.temp}\nrecieved on:{self.timestamp}"

class HumidityReadings(models.Model):
    id = models.AutoField(primary_key=True) 
    device=models.ForeignKey(Device,on_delete=models.CASCADE)
    humid=models.FloatField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Humidity: {self.humid}\nrecieved on:{self.timestamp}"
    