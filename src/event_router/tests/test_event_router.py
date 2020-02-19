from django.test import TestCase, Client
from rest_framework.reverse import reverse


class HashingTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        cls.event_push_url = reverse('event_router:event-router')

    def setUp(self):

        # self.client = Client()
        # self.apsalar_webhook = reverse('core:apsalar-webhook')

    def test_post_events(self):
        # PartitionHashing.get_partition()