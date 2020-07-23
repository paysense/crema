import atexit
import json
import logging
import time
import uuid

from kafka import KafkaProducer
from kafka.errors import KafkaError

from crema.decorators import singleton
from .config import ENABLED, KAFKA_BOOTSTRAP_SERVERS
from .exceptions import KafkaException
from .hashing import PartitionHashing

LOGGER = logging.getLogger("kafka_util")


@singleton
class KafkaUtil:
    """
    This util is responsible for pushing data successfully to Kafka cluster and it also manages the success
    and failure callbacks. Producer is initialized as a class variable so that we don't keep making connection
    on every api call
    """

    def __init__(self, kafka_vars=None):
        self._kafka_producer = None
        self.kafka_vars = kafka_vars or {}

    def flush_messages(self):
        # it should be registered at atexit only after KafkaProducer gets initialized. KafkaProducer has its own
        # set of cleanup functions registered at atexit e.g. closing kafka connection. This function should be executed
        # at first among other registered function as it needs kafka connection to send buffered events to kafka
        if self._kafka_producer:
            self._kafka_producer.flush()


    @property
    def producer(self):
        # initialise kafkaProducer only when its about to send events. It avoids creating unnecessary connection
        # to kafka cluster.
        if self._kafka_producer is None:
            self._kafka_producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                api_version=(8,),
                **self.kafka_vars
            )
            atexit.register(self.flush_messages)
        return self._kafka_producer

    def _success_callback(self, data, record_metadata):
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

    def _error_callback(self, data, partition, exception):
        if isinstance(exception, KafkaError):
            msg = "{e}, partition: {partition}, data: {data}".format(
                e=str(exception), partition=partition, data=data
            )
            LOGGER.exception(msg)
            raise KafkaException(msg)
        else:
            raise exception

    def push_async(self, data):
        """
        It pushed data asynchronously to kafka servers. It is useful when data is sent in a api call.
        Args:
            data:

        Returns:

        """
        if ENABLED is False:
            LOGGER.info("Please set ENABLE_KAFKA env variable to True to push events")
            return

        uid = str(uuid.uuid4())
        start_time = time.time()
        event_type = data["meta_data"]["event_type"]
        if event_type == 'SMS':
            device_id = data["meta_data"]["device_id"]
            partition = PartitionHashing.get_partition(device_id, event_type)
        else:
            master_user_id = data["meta_data"]["user_id"]
            partition = PartitionHashing.get_partition(master_user_id, event_type)
        LOGGER.debug(
            "time take to get partition for uid:{uid} {t}".format(
                uid=uid, t=(time.time() - start_time)
            )
        )

        start_time = time.time()
        self.producer.send(event_type, data, partition=partition,).add_callback(
            self._success_callback, data
        ).add_errback(self._error_callback, data, partition)
        LOGGER.debug(
            "time take to publish for uid:{uid} {t}".format(
                uid=uid, t=(time.time() - start_time)
            )
        )

    def push(self, data):
        if ENABLED is False:
            LOGGER.info("Please set ENABLE_KAFKA env variable to True to push events")
            return

        event_type = data["meta_data"]["event_type"]
        if event_type == 'SMS':
            device_id = data["meta_data"]["device_id"]
            partition = PartitionHashing.get_partition(device_id, event_type)
        else:
            master_user_id = data["meta_data"]["user_id"]
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
