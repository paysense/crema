import json
import logging

from kafka import KafkaProducer
from kafka.errors import KafkaError

from .config import ENABLED, KAFKA_BOOTSTRAP_SERVERS
from .exceptions import KafkaException
from .hashing import PartitionHashing

LOGGER = logging.getLogger("kafka_util")


class KafkaUtil:
    """
    This util is responsible for pushing data successfully to Kafka cluster and it also manages the success
    and failure callbacks. Producer is initialized as a class variable so that we don't keep making connection
    on every api call
    """

    def __init__(self):
        self.producer = None

    def push(self, data):
        if ENABLED is False:
            LOGGER.info("Please set ENABLE_KAFKA env variable to True to push events")
            return

        if self.producer is None:
            # initialise kafkaProducer only when its about to send events. It avoids creating unnecessary connection
            # to kafka cluster.
            self.producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                api_version=(8,),
            )

        master_user_id = data["meta_data"]["user_id"]
        event_type = data["meta_data"]["event_type"]
        partition = PartitionHashing.get_partition(master_user_id, event_type)

        future = self.producer.send(event_type, data, partition=partition,)
        try:
            record_metadata = future.get(timeout=10)
            # not using f"" style as python 3.4 is used at AMS and doesn't support this style
            LOGGER.debug(
                (
                    "Successfully published data: {data}, with topic: {topic}, on partition: "
                    "{partition} with offset: {offset}"
                ).format(
                    data=data,
                    topic=record_metadata.topic,
                    partition=record_metadata.partition,
                    offset=record_metadata.offset,
                )
            )
        except KafkaError as e:
            msg = "{e}, partition: {partition}, data: {data}".format(
                e=str(e), partition=partition, data=data
            )
            LOGGER.exception(msg)
            raise KafkaException(msg)


kafka_util = KafkaUtil()
