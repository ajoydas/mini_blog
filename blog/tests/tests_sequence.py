from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SequenceTestCase(APITestCase):
    """
    This testcase tests the sequence of API calls showed in the sequence diagram.
    """

    def setUp(self):
        self.reader = User.objects.create_user(username='reader', password='readerpass')
        self.reader.profile.role = 'Reader'
        self.reader.save()
        self.author = User.objects.create_user(username='author', password='authorpass')
        self.author.profile.role = 'Author'
        self.author.save()
        self.admin = User.objects.create_user(username='admin', password='adminpass')
        self.admin.profile.role = 'Admin'
        self.admin.save()

        self.reader.password, self.author.password, self.admin.password = 'readerpass', 'authorpass', 'adminpass'

    def login_user_with_validation(self, user):
        response = self.client.post(reverse('login'),
                                    {'username': user.username, 'password': user.password})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        return response.data['access']

    def test_sequence(self):
        """
        Author
        """
        # login
        access_token = self.login_user_with_validation(self.author)

        # create post
        post_data = {'title': 'New Post', 'body': 'New Body'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.post(reverse('post-list'), post_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'New Post')
        self.assertEqual(response.data['body'], 'New Body')
        post_data['post_id'] = response.data['post_id']

        """
        Reader
        """
        # login
        access_token = self.login_user_with_validation(self.reader)

        # Retrieve post
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.get(reverse('post-detail', args=[post_data['post_id']]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], post_data['title'])
        self.assertEqual(response.data['body'], post_data['body'])

        # Create comment
        comment_data = {'body': 'New Comment', 'post_id': post_data['post_id']}
        response = self.client.post(reverse('comment-route'), comment_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['body'], comment_data['body'])
        comment_data['comment_id'] = response.data['comment_id']

        """
        Admin
        """
        # login
        access_token = self.login_user_with_validation(self.admin)

        # Update post
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        post_data['title'] = 'Updated Post'
        post_data['body'] = 'Updated Body'
        response = self.client.put(reverse('post-detail', args=[post_data['post_id']]), post_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], post_data['title'])
        self.assertEqual(response.data['body'], post_data['body'])
