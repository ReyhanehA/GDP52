import sys
import re
from collections import defaultdict

import monocle
from monocle import _o, Return
monocle.init(sys.argv[1])

from monocle.stack import eventloop
from monocle.stack.network import add_service
from monocle.stack.network.http import HttpServer


app = HttpServer(8888)


@app.get('/')
def index(req):
    yield Return(200, {'yes': 'indeed'}, "hello")


@app.post('/slashable/?')
def slashable(req):
    yield Return("slashable!")


@app.get('/first/:first/second/:second_what')
def params(req, first=None, second_what=None):
    yield Return("first: %s\nsecond: %s\n" % (first, second_what))


@app.get(re.compile('/re/[^x]'))
def regexp(req):
    yield Return("regexp!")


@app.get('/*/star/*')
def stars(req):
    yield Return("star!")


add_service(app)
eventloop.run()
