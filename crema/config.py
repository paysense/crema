import os


kafka_servers = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
KAFKA_BOOTSTRAP_SERVERS = kafka_servers.split(",")

# flag to enable/disable kafka on a particular service that is using this library,
# this will give control after integration where the service can decide to stop the kafka message push with this flag
ENABLED = os.environ.get("ENABLE_KAFKA", "False").lower() == 'true'

# wait time to get response from kafka
RESULT_WAIT_TIME = 1  # in seconds
