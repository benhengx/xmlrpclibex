#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from xmlrpclibex import xmlrpclibex


# your test proxy config
http_proxy = {
    'host':         '127.0.0.1',
    'port':         '9667'
}

socks_proxy = {
    'host':         '127.0.0.1',
    'port':         '8080',
    'is_socks':     True,
}

class TestXmlrpcEx(unittest.TestCase):
    def test_http_over_http_proxy(self):
        xs = xmlrpclibex.ServerProxy('http://pypi.python.org/pypi', 
                                    proxy=http_proxy,
                                    timeout=30)
        rd = xs.release_data('game24', '1.0.0')
        xs('close')()
        self.assertEqual('game24', rd['name'])

    def test_http_over_socks_proxy(self):
        xs = xmlrpclibex.ServerProxy('http://pypi.python.org/pypi', 
                                    proxy=socks_proxy,
                                    timeout=30)
        rd = xs.release_data('game24', '1.0.0')
        xs('close')()
        self.assertEqual('game24', rd['name'])

    def test_https_over_http_proxy(self):
        xs = xmlrpclibex.ServerProxy('https://pypi.python.org/pypi', 
                                    proxy=http_proxy,
                                    timeout=30)
        rd = xs.release_data('game24', '1.0.0')
        xs('close')()
        self.assertEqual('game24', rd['name'])

    def test_https_over_socks_proxy(self):
        xs = xmlrpclibex.ServerProxy('https://pypi.python.org/pypi', 
                                    proxy=socks_proxy,
                                    timeout=30)
        rd = xs.release_data('game24', '1.0.0')
        xs('close')()
        self.assertEqual('game24', rd['name'])


if __name__ == '__main__':
    unittest.main()
