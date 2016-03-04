"""
The MIT License (MIT)

Copyright (c) 2015 codebolab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__author__ = "Jose Maria Zambrana Arze <contact@josezambrana.com>"
__copyright__ = "Copyright 2014, code.bo"


import logging
import json

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


class TestBase(TestCase):
    def setUp(self):
        self.logger = logging.getLogger('project.verbose')

    def _info(self, message):
        self.logger.info(message)


class TestViews(TestBase):
    secure = False
    login_data = {
        'username': 'admin',
        'password': '.admin'
    }

    # Some libraries like Django rest framework use a token to authenticate, it
    # can be defined here.
    token = ""

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('admin:login')
        self.logout_url = reverse('admin:logout')
        super(TestViews, self).setUp()

    def _login(self, data=None):
        if data is None:
            data = self.login_data

        response = self.post(self.login_url, data)
        assert response.status_code == 302
        return response

    def _logout(self):
        response = self.get(self.logout_url)
        assert response.status_code == 302
        return response

    def request(self, method, path, *args, **kwargs):
        if self.secure:
            kwargs['wsgi.url_scheme'] = 'https'

        method = method.lower()

        if method == 'get':
            return self.client.get(path, *args, **kwargs)
        if method == 'post':
            return self.client.post(path, *args, **kwargs)
        if method == 'put':
            return self.client.put(path, *args, **kwargs)
        if method == 'delete':
            return self.client.delete(path, *args, **kwargs)

        raise ValueError

    def auth_request(self, method, path, *args, **kwargs):
        """
        Method to send valid requests to django rest framework with
        the authentication token.
        """

        token = kwargs.pop('token', self.token)
        kwargs['HTTP_AUTHORIZATION'] = 'Token %s' % token

        return self.request_ajax(method, path, *args, **kwargs)

    def request_ajax(self, method, path, *args, **kwargs):
        kwargs['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'

        if method in ('post', 'put') and kwargs.get('format') != 'multipart':
            kwargs['content_type'] = 'application/json'
            data = kwargs.get('data', {})
            kwargs['data'] = json.dumps(data)

        response = self.request(method, path, *args, **kwargs)
        self._info('%s-%s> %s' % (method, response.status_code, path))

        self._info('response: %s' % response.content)
        if response.status_code != 204:
            try:
                content = response.content.decode("utf-8")
            except TypeError:
                content = response.content

            return response.status_code, json.loads(content)

        return 204, None

    def get(self, path, *args, **kwargs):
        return self.request('get', path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return self.request('post', path, *args, **kwargs)

    def put(self, path, *args, **kwargs):
        return self.request('put', path, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        return self.request('delete', path, *args, **kwargs)

    def get_ajax(self, path, *args, **kwargs):
        return self.request_ajax('get', path, *args, **kwargs)

    def post_ajax(self, path, *args, **kwargs):
        return self.request_ajax('post', path, *args, **kwargs)

    def put_ajax(self, path, *args, **kwargs):
        return self.request_ajax('put', path, *args, **kwargs)

    def delete_ajax(self, path, *args, **kwargs):
        return self.request_ajax('delete', path, *args, **kwargs)
