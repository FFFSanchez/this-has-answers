from http import HTTPStatus

import requests
from django.test import TestCase


class ApiURLTests(TestCase):

    URL = 'http://127.0.0.1:8000/api/v1/compute/'

    def test_get(self):
        """Проверяем доступность сервиса."""
        response = requests.get(ApiURLTests.URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post(self):
        """Проверяем минимальную работоспособность."""
        response = requests.post(
            ApiURLTests.URL,
            json={"expression": "lg(5*a+2*b)", "varies": {"a": "2", "b": "3"}}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_check_answer(self):
        """Проверяем корректность ответа."""
        response = requests.post(
            ApiURLTests.URL,
            json={"expression": "lg(5*a+2*b^21+tan(9)+tan(2))",
                  "varies": {"a": "2", "b": "3"}}
        )
        self.assertEqual(response.json()["result"], "10.320576344929734")
