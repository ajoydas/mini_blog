import time

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class PostCreationRateThrottleTestCase(APITestCase):
    """
    This testcase tests the rate limiting on post creation.
    """

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.user.profile.role = 'Author'
        self.user.save()

    def test_post_creation_rate_limit(self):
        url = reverse('post-list')
        data = {'title': 'New Post', 'body': 'New Body'}
        self.client.force_authenticate(user=self.user)

        # Send POST requests one after the other
        for i in range(5):
            response = self.client.post(url, data)

            if i < 3:
                # This number of requests should return a successful response
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            else:
                # These request should be rate-limited and return a 429 status code
                self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS, 'Rate throttling failed.')

            time.sleep(1)
