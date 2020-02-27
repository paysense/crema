# crema
This is a light weight generic library which is used to push events to kafka. This package serves below purpose:
 - It makes sure that only whitelisted event types/topic are pushed to kafka across our organisation
 - It takes care of event routing to partitions. It uses consistent hashing to ensure that all the data of user belonging to a event type goes to the same partition always. In case of changing number of partition, we need shuffle least amount of data.
 
### How to use it
You need to define below variables in your environment
 - `ENABLE_KAFKA=true` (by default, it will be `False`)
 - `KAFKA_BOOTSTRAP_SERVERS=localhost1:9092,localhost2:9092` (`,` separated kafka server IP address)
 
 ```python
import time
from crema import kafka_util, EventType

 
data = {
    "meta_data": {
         "master_user_id": <master_user_id>,
         "event_type": <EventType.LOAN_APPLICATION.value>,
         "ts": time.time()
     },
     "payload": {
          "var1": "val1",
          "var2": "val2"
     }
}

kafka_util.push(data)
```
