from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from unittest.mock import patch
from .views import CreateCheckoutSessionView


class CreateCheckoutSessionViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', password='testpass')

    def test_create_checkout_session(self):
        request = self.factory.get(
            reverse('create_checkout_session', kwargs={'slug': 'hard-coded-slug'}))
        request.user = self.user

        with patch('stripe.checkout.Session.create') as create_session:
            create_session.return_value.id = 'test-session-id'
            response = CreateCheckoutSessionView.as_view()(request, slug='hard-coded-slug')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {
                             'id': 'test-session-id'})
