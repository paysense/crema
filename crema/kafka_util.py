import json
import logging

from kafka.errors import KafkaError

from .config import ENABLED, KAFKA_BOOTSTRAP_SERVERS
from kafka import KafkaProducer

from .exceptions import KafkaException
from .hashing import PartitionHashing

LOGGER = logging.getLogger('kafka_util')


class KafkaUtil:
    """
    This util is responsible for pushing data successfully to Kafka cluster and it also manages the success
    and failure callbacks. Producer is initialized as a class variable so that we don't keep making connection
    on every api call
    """

    def __init__(self):
        if ENABLED is True:
            self.producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                api_version=(8,),
            )

    def push(self, data):
        if ENABLED is False:
            LOGGER.info("Please set ENABLE_KAFKA env variable to True to push events")
            return

        master_user_id = data["meta_data"]["master_user_id"]
        event_type = data["meta_data"]["event_type"]
        partition = PartitionHashing.get_partition(master_user_id)

        payload = data["payload"]

        future = self.producer.send(event_type, data, partition=partition,)
        try:
            record_metadata = future.get(timeout=10)
            LOGGER.debug(
                f"Successfully published data: {data}, with topic: {record_metadata.topic}, on partition: "
                f"{record_metadata.partition} with offset: {record_metadata.offset}"
            )
        except KafkaError as e:
            msg = f"{str(e)}, partition: {partition}, data: {data}"
            LOGGER.exception(msg)
            raise KafkaException(msg)


kafka_util = KafkaUtil()
