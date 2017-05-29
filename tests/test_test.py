import unittest
import json

from app import db, create_app

from tests import APITestCase
from tests.school.factories import SchoolFactory

from app.user.models import Form
from tests.user.factories import FormFactory, UserFactory

school_factory = SchoolFactory()
form_factory = FormFactory()
user_factory = UserFactory()


class TestTestCase(APITestCase):
    def test_hitting_self(self):
        resp = self.client.get('/user/')
        import ipdb; ipdb.set_trace()
        self.assertEqual(resp.status_code, 200)
