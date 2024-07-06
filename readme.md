## <h1 align='center'> IOT-Device Tracker Application</h1>

## API calls as follows :

### <a> api/devices/ </a> - methods {POST: Create a new device , GET : List all devices}

### <a> api/devices/{device_id} </a> - methods {GET: Retrieve a device , DELETE : Delete a device}

### <a> api/devices/{deviceuid}/readings/{parameter}/?start_on=yyyy-mm-ddTHH:MM:SS&end_on=yyyy-mm-ddTHH:MM:SS </a> - methods {GET: Returns the readings of a device in a given period}

### <a> devices-graph/</a>- methods {GET: Returns a graph of a device (Temperature & Humidity ) vs Time}
