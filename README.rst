===========
xmlrpclibex
===========

A Python xmlrpc client library with proxy and timeout support.

Installation
------------

.. code-block:: bash

    $ pip install xmlrpclibex

Or

.. code-block:: bash

    $ python setup.py install

Usage
-----

* A basic example

.. code-block:: python

    from xmlrpclibex import xmlrpclibex
    sp = xmlrpclibex.ServerProxy(uri, timeout=30, 
                        proxy={
                            'host': 'your proxy address',
                            'port': 'your proxy port',
                            'is_socks': True,
                            'socks_type': 'v5'
                        })

* The timeout and proxy parameters

  This module subclasses the ServerProxy class from the xmlrpclib module (or
  the xmlrpc.client module in case of Python3), and adds two parameters
  timeout and proxy.

  * timeout: seconds waiting for the socket operations.
  * proxy: a dict specifies the proxy settings (supports HTTP proxy and socks
    proxy). The dict supports the following keys:

    * host: the address of the proxy server (IP or DNS)
    * port: the port of the proxy server. default: 8080 for http
      proxy, and 1080 for socks proxy
    * username: username to authenticate to the server. default None
    * password: password to authenticate to the server, only relevant when
      username is set. default None
    * is_socks: whether the proxy is a socks proxy, default False
    * socks_type: string, 'v4', 'v5', 'http' (http connect tunnel), only 
      relevant when is_socks is True. default 'v5'

Note
-------

* Sometimes, access HTTPS over HTTP Proxy (through CONNECT tunnel) may report
  errors, recommend using SOCKS proxy.

License
-------

Copyright 2015 benhengx

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
