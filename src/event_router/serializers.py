from rest_framework import serializers

from event_router.choices import EventType
from event_router.utils.kafka_util import KafkaUtil


class EventMetaDataSerializer(serializers.Serializer):
    event_type = serializers.ChoiceField(choices=EventType.choices)
    master_user_id = serializers.IntegerField(min_value=1)
    ts = serializers.IntegerField(min_value=0)


class EventSerializer(serializers.Serializer):
    meta_data = EventMetaDataSerializer()
    payload = serializers.DictField()

    def save(self):
        data = self.validated_data
        kafka_util = KafkaUtil()
        kafka_util.push(data)

