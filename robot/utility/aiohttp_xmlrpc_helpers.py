'''aiohttp xmlrpc helpers

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''
import io
import base64

import numpy
from lxml import etree
from aiohttp_xmlrpc.common import py2xml, XML2PY_TYPES

@py2xml.register(numpy.ndarray)
def _(value):
    el = etree.Element('numpy.ndarray')
    memfile = io.BytesIO()
    numpy.save(memfile, value)
    memfile.seek(0)
    el.text = base64.b64encode(memfile.read()) 
    return el

def numpy_ndarray(x):
    memfile = io.BytesIO()
    memfile.write(base64.b64decode(x.text))
    memfile.seek(0)
    return numpy.load(memfile)

XML2PY_TYPES["numpy.ndarray"] = numpy_ndarray

