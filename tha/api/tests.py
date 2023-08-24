from http import HTTPStatus

from django.test import Client, TestCase


class ApiURLTests(TestCase):
    """ Минимальный смоук тест """

    URL = '/api/compute/'

    def setUp(self):
        self.guest_client = Client()

    def test_get(self):
        """Проверяем доступность сервиса."""
        response = self.guest_client.get(ApiURLTests.URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post(self):
        """Проверяем минимальную работоспособность."""
        response = self.guest_client.post(
            ApiURLTests.URL,
            data={"expression": "lg(5*a+2*b)", "varies": {"a": "2", "b": "3"}},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_check_answer(self):
        """Проверяем корректность ответа."""
        response = self.guest_client.post(
            ApiURLTests.URL,
            data={"expression": "lg(5*a+2*b^21+tan(9)+tan(2))",
                  "varies": {"a": "2", "b": "3"}},
            content_type='application/json'
        )
        self.assertEqual(response.json()["result"], "10.320576344929734")
