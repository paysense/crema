from uhashring import HashRing
from .choices import EventPartition


class PartitionHashing:

    @classmethod
    def get_partition(cls, key, event_type):
        consistent_hashing = HashRing(nodes=list(range(EventPartition[event_type].value)))
        return consistent_hashing.get_node(key)
