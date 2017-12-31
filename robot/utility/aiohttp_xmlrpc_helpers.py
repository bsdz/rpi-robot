'''aiohttp xmlrpc helpers

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''
import io
import json

import numpy
from lxml import etree
from aiohttp_xmlrpc.common import py2xml, XML2PY_TYPES

@py2xml.register(numpy.ndarray)
def _(value):
    el = etree.Element('numpy.ndarray')
    memfile = io.BytesIO()
    numpy.save(memfile, value)
    memfile.seek(0)
    el.text = json.dumps(memfile.read().decode('latin-1'))
    return el


