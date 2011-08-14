from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import urllib, threading, cgi
try:
    import simplejson as json
    assert json
except ImportError:
    import json
import sys

class acquired(object):
    def __init__(self, cv):
        self.cv = cv
    def __enter__(self):
        self.cv.acquire()
    def __exit__(self, *args, **kw):
        self.cv.release()

# inspired by http://fragments.turtlemeat.com/pythonwebserver.php
class Monitor(HTTPServer, ThreadingMixIn):

    __thread = None
    __cv = None

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            query = urllib.splitquery(self.path)[1]
            length = int(self.headers.getheader('content-length'))
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-length'))

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            assert ctype == 'application/x-www-form-urlencoded'
            b = self.rfile.read(length)
            vars = cgi.parse_qs(b, keep_blank_values=1)
            print '****** POST ********'
            for p in vars['packets']:
                self.server.add_messages(json.loads(p))
            # Begin the response
            self.send_response(200)
            self.end_headers()



    def __init__(self):
        HTTPServer.__init__(self, ('',8087), Monitor.Handler)
        self.__cv = threading.Condition()
        self.__thread = threading.Thread(target=self.serve_forever)
        self.__messages = []
        self.__thread.setDaemon(True)
        self.__thread.start()


    def add_messages(self, messages):
        for m in messages:
            print '==> ', m['event'] # 8*' ', m['payload']

        with acquired(self.__cv):
            self.__messages += messages
            self.__cv.notify()

    def messages(self):
        while 1:
            yield self.next_message()

    def next_message(self):
        with acquired(self.__cv):
            while len(self.__messages) == 0:
                self.__cv.wait()
            return self.__messages.pop(0)

    def __del__(self):
        if self.__thread:
            self.shutdown()
