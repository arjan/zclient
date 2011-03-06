# Copyright 2011 Arjan Scherpenisse <arjan@scherpenisse.net>
# See LICENSE for details.

# Based on client.py from python-oauth, Copyright (c) 2007 Leah Culver

import sys
import os
import ConfigParser
import httplib
import time
import oauth.oauth as oauth

try:
    import json
except ImportError:
    import simplejson as json


class ApplicationRegistry (object):

    def __init__(self, fn=None):
        self.setFilename(fn)

    def setFilename(self, fn):
        self.filename = os.path.expanduser(fn)
        self.parser = ConfigParser.ConfigParser()
        self.parser.read(self.filename)

    def getApps(self):
        return [s[4:] for s in self.parser.sections() if s[:4] == "app:"]

    def getClients(self):
        return [s[7:] for s in self.parser.sections() if s[:7] == "client:"]

    def addApp(self, id, host, ckey, csec):
        k = 'app:'+id
        self.parser.add_section(k)
        self.parser.set(k, 'host', host)
        self.parser.set(k, 'ckey', ckey)
        self.parser.set(k, 'csec', csec)

    def removeApp(self, id):
        k = 'app:'+id
        self.parser.remove_section(k)

    def addClient(self, id, app, tkey, tsec):
        k = 'client:'+id
        self.parser.add_section(k)
        self.parser.set(k, 'app', app)
        self.parser.set(k, 'tkey', tkey)
        self.parser.set(k, 'tsec', tsec)

    def removeClient(self, id):
        k = 'client:'+id
        self.parser.remove_section(k)

    def getApp(self, id):
        return dict(self.parser.items("app:"+id))

    def getClient(self, id):
        client = dict(self.parser.items("client:"+id))
        app = self.getApp(client['app'])
        app['id'] = client['app']
        client['app'] = app
        return client
    
    def showAll(self):
        print "%-20s %s" % ("App", "Host")
        print "--------------------------------------"
        for app in self.getApps():
            a = self.getApp(app)
            print "%-20s %s   " % (app, a['host'])
        print
        print "%-20s %s" % ("Client", "App")
        print "--------------------------------------"
        for client in self.getClients():
            c = self.getClient(app)
            print "%-20s %s   " % (client, c['app']['id'])
        print

    def save(self):
        self.parser.write(open(self.filename, 'w'))

    def getZotonicClient(self, client_id):
        client = self.getClient(client_id)
        return ZotonicClient(client)



class OAuthException(Exception):
    pass

class ZotonicClient(oauth.OAuthClient):

    def __init__(self, client_or_app):
        if 'app' in client_or_app:
            self.app = client_or_app['app']
            self.client = client_or_app
        else:
            self.app = client_or_app
            self.client = None

        self.request_token_url = 'http://%s/oauth/request_token' % self.app['host']
        self.authorization_url = 'http://%s/oauth/authorize' % self.app['host']
        self.access_token_url = 'http://%s/oauth/access_token' % self.app['host']
        self.connection = httplib.HTTPConnection(self.app['host'])
        self.signature_method = oauth.OAuthSignatureMethod_PLAINTEXT()
        #self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
        self.consumer = oauth.OAuthConsumer(self.app['ckey'], self.app['csec'])

    def fetch_request_token(self):
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, callback='oob', http_url=self.request_token_url)
        oauth_request.sign_request(self.signature_method, self.consumer, None)
        self.connection.request(oauth_request.http_method, self.request_token_url, headers=oauth_request.to_header()) 
        response = self.connection.getresponse()
        if response.status >= 400:
            raise OAuthException(response.read())
        return oauth.OAuthToken.from_string(response.read())

    def fetch_access_token(self):
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=token, verifier='', http_url=self.access_token_url)
        oauth_request.sign_request(self.signature_method, self.consumer, token)
        self.connection.request(oauth_request.http_method, self.access_token_url, headers=oauth_request.to_header()) 
        response = self.connection.getresponse()
        if response.status >= 400:
            raise OAuthException(response.read())
        return oauth.OAuthToken.from_string(response.read())

    def doMethod(self, method, parameters={}):
        if parameters:
            encoded_params = "?" + ("&".join(["%s=%s" % (oauth.escape(k), oauth.escape(v)) for k,v in parameters.iteritems()]))
        else:
            encoded_params = ""
        url = 'http://%s/api/%s%s' % (self.app['host'], method, encoded_params)
        token = oauth.OAuthToken(self.client['tkey'], self.client['tsec'])
        oauth_request = oauth.OAuthRequest.from_consumer_and_token(self.consumer, token=token, http_method='GET', http_url=url, parameters=parameters)
        oauth_request.sign_request(self.signature_method, self.consumer, token)

        self.connection.request(oauth_request.http_method, url, headers=oauth_request.to_header()) 
        response = self.connection.getresponse()
        if response.status >= 400:
            raise OAuthException(response.read())

        decoded = json.loads(response.read())
        return decoded


    def register_client(self, callback=None):

        # fetch request token
        token = self.fetch_request_token()

        oauth_request = oauth.OAuthRequest.from_token_and_callback(token=token, http_url=self.authorization_url)
        url = oauth_request.to_url()

        if callback is None:
            def wait_for_url(url):
                print "*" * 60
                print "Please go to the following URL to authorize your request."
                print "When you're done, press ENTER here to finish."
                print
                print ">>> ", url
                print
                print "*" * 60
                sys.stdin.readline()
            callback = wait_for_url

        callback(url)

        # get access token
        token = self.fetch_access_token()
        return token

