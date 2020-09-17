import pytest
import requests_mock
from requests import HTTPError

from app.utils.webhook import notify_webhook


def test_call_webhook(app, requests_mock):
    with app.app_context():
        url = 'http://example.com/web/hook'
        app.config['API_WEBHOOK_URL'] = url
        requests_mock.get(url, json= {'it': 'worked'})
        resp = notify_webhook()
        assert requests_mock.call_count == 1
        assert resp.json() == {'it': 'worked'}

        requests_mock.get(url, status_code=500)
        resp = notify_webhook()
        assert requests_mock.call_count == 2

        # try with a bad url/error in request
        requests_mock.register_uri('GET', url, exc=HTTPError),
        resp = notify_webhook()
        assert resp == False
