import json
import logging

from django.conf import settings
from kafka import KafkaProducer

from event_router.utils.hashing import PartitionHashing

LOGGER = logging.getLogger(__name__)


class KafkaUtil:
    """
    This util is responsible for pushing data successfully to Kafka cluster and it also manages the success
    and failure callbacks. Producer is initialized as a class variable so that we don't keep making connection
    on every api call
    """

    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    def on_send_success(self, data, record_metadata):
        LOGGER.debug(
            f"Successfully published data: {data}, with topic: {record_metadata.topic}, on partition: "
            f"{record_metadata.partition} with offset: {record_metadata.offset}"
        )

    def on_send_error(self, data, partition, exception):
        msg = f"{str(exception)}, msg: {exception.description}, partition: {partition}, data: {data}"
        LOGGER.exception(msg)

    def push(self, data):
        master_user_id = data["meta_data"]["master_user_id"]
        event_type = data["meta_data"]["event_type"]
        partition = PartitionHashing.get_partition(master_user_id)

        payload = data["payload"]
        self.producer.send(event_type, payload, partition=partition,).add_callback(
            self.on_send_success, data
        ).add_errback(self.on_send_error, data, partition)
