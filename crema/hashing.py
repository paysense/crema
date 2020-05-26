from uhashring import HashRing
from .choices import EventPartition


class PartitionHashing:

    _hash_rings_dict = {}

    @classmethod
    def get_hash_ring(cls, event_type):
        if event_type in cls._hash_rings_dict:
            return cls._hash_rings_dict[event_type]
        cls._hash_rings_dict[event_type] = HashRing(
            nodes=list(range(EventPartition[event_type].value))
        )
        return cls._hash_rings_dict[event_type]

    @classmethod
    def get_partition(cls, key, event_type):
        consistent_hashing = cls.get_hash_ring(event_type)
        return consistent_hashing.get_node(key)
