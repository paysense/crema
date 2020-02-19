from django.test import TestCase


class HashingTest(TestCase):
    def setUp(self):
        pass
        # self.client = Client()
        # self.apsalar_webhook = reverse('core:apsalar-webhook')

    def test_get_same_partition(self):
        PartitionHashing.get_partition()