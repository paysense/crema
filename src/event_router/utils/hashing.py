from uhashring import HashRing

from event_router.constants import PARTITIONS


class PartitionHashing:

    consistent_hashing = HashRing(nodes=list(range(PARTITIONS)))

    @classmethod
    def get_partition(cls, key):
        return cls.consistent_hashing.get_node(key)
