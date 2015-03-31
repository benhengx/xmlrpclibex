
from __future__ import absolute_import, print_function, division

import socket
import base64
import ssl
try:
    import httplib
    import xmlrpclib
    from urllib import splittype
except ImportError:
    import http.client as httplib
    import xmlrpc.client as xmlrpclib
    from urllib.parse import splittype

import socks


def init_socks(proxy, timeout):
    '''init a socks proxy socket.'''
    map_to_type = {
        'v4':   socks.SOCKS4,
        'v5':   socks.SOCKS5,
        'http': socks.HTTP
    }
    ssock = socks.socksocket()
    if isinstance(timeout, (int, float)):
        ssock.settimeout(timeout)
    ssock.set_proxy(proxy_type=map_to_type[proxy.get('socks_type', 'v5')],
                    rdns=proxy.get('rdns', True),
                    addr=proxy.get('host'), 
                    port=proxy.get('port'), 
                    username=proxy.get('username'), 
                    password=proxy.get('password'))
    return ssock


class SocksProxiedHTTPConnection(httplib.HTTPConnection):
    '''Proxy the http connection through a socks proxy.'''

    def init_socks(self, proxy):
        self.ssock = init_socks(proxy, self.timeout)

    def connect(self):
        self.ssock.connect((self.host, self.port))
        self.sock = self.ssock


class SocksProxiedHTTPSConnection(httplib.HTTPSConnection):
    '''Proxy the https connection through a socks proxy.'''

    def init_socks(self, proxy):
        self.ssock = init_socks(proxy, self.timeout)

    def connect(self):
        self.ssock.connect((self.host, self.port))
        self.sock = ssl.wrap_socket(self.ssock, self.key_file, self.cert_file,
                        ssl_version=ssl.PROTOCOL_TLSv1)

    def close(self):
        httplib.HTTPSConnection.close(self)

        if self.ssock:
            self.ssock.close()
            self.ssock = None


class TransportWithTo(xmlrpclib.Transport):
    '''Transport support timeout'''

    cls_http_conn = httplib.HTTPConnection
    cls_https_conn = httplib.HTTPSConnection

    def __init__(self, use_datetime=0, is_https=False, timeout=None):
        xmlrpclib.Transport.__init__(self, use_datetime)

        self.is_https = is_https
        if timeout is None:
            timeout = socket._GLOBAL_DEFAULT_TIMEOUT
        self.timeout = timeout

    def make_connection(self, host):
        if self._connection and host == self._connection[0]:
            return self._connection[1]

        # create a HTTP/HTTPS connection object from a host descriptor
        # host may be a string, or a (host, x509-dict) tuple
        chost, self._extra_headers, x509 = self.get_host_info(host)

        #store the host argument along with the connection object
        if self.is_https:
            self._connection = host, self.cls_https_conn(chost,
                    None, timeout=self.timeout, **(x509 or {}))
        else:
            self._connection = host, self.cls_http_conn(chost,
                    timeout=self.timeout)
        return self._connection[1]


class ProxiedTransportWithTo(TransportWithTo):
    '''Transport supports timeout and http proxy'''

    def __init__(self, proxy, use_datetime=0, timeout=None):
        TransportWithTo.__init__(self, use_datetime, False, timeout)

        self.proxy_addr = '%s:%s' % (proxy['host'], proxy.get('port', 8080))
        if proxy.get('username') and proxy.get('password'):
            self.proxy_cred = base64.encodestring('%s:%s' % (proxy['username'], proxy['password']))
        else:
            self.proxy_cred = ''

    def request(self, host, handler, request_body, verbose=False):
        realhandler = 'http://%s%s' % (host, handler)
        return TransportWithTo.request(self, host, realhandler, request_body, verbose)

    def make_connection(self, host):
        return TransportWithTo.make_connection(self, self.proxy_addr)

    def send_content(self, connection, request_body):
        if self.proxy_cred:
            connection.putheader('Proxy-Authorization', 'Basic ' + self.proxy_cred)
        return TransportWithTo.send_content(self, connection, request_body)


class SocksProxiedTransportWithTo(TransportWithTo):
    '''Transport supports timeout and socks v4/v5 and http connect tunnel'''

    cls_http_conn = SocksProxiedHTTPConnection
    cls_https_conn = SocksProxiedHTTPSConnection

    def __init__(self, proxy, use_datetime=0, is_https=False, timeout=None):
        TransportWithTo.__init__(self, use_datetime, is_https, timeout)

        self.proxy = proxy

    def make_connection(self, host):
        conn = TransportWithTo.make_connection(self, host)
        conn.init_socks(self.proxy)
        return conn


class ServerProxy(xmlrpclib.ServerProxy):
    """New added keyword arguments
    timeout: seconds waiting for the socket
    proxy: a dict specify the proxy settings, it supports the following fields:
        host: the address of the proxy server (IP or DNS)
        port: the port of the proxy server. default: 8080 for http
              proxy, and 1080 for socks proxy
        username: username to authenticate to the server. default None
        password: password to authenticate to the server, only relevant when
                  username is set. default None
        is_socks: whether the proxy is a socks proxy, default False
        socks_type: string, 'v4', 'v5', 'http' (http connect tunnel), only 
                    relevant when is_socks is True. default 'v5'
    """

    def __init__(self, uri, transport=None, encoding=None, verbose=0,
                 allow_none=0, use_datetime=0, timeout=None, proxy=None):

        if transport is None and (timeout or proxy):
            is_https = splittype(uri)[0] == 'https'

            if proxy is None:
                transport = TransportWithTo(use_datetime, is_https, timeout)
            else:
                if proxy.get('port'):
                    proxy['port'] = int(proxy['port'])

                if is_https and not proxy.get('is_socks', False):
                    # https must be tunnelled through http connect
                    proxy['is_socks'] = True
                    proxy['socks_type'] = 'http'

                if not proxy.get('is_socks', False):
                    transport = ProxiedTransportWithTo(proxy, use_datetime, 
                                timeout)
                else:
                    transport = SocksProxiedTransportWithTo(proxy, use_datetime, 
                                is_https, timeout)

        xmlrpclib.ServerProxy.__init__(self, uri, transport, encoding, verbose,
                allow_none, use_datetime)

