'''aiohttp xmlrpc helpers

rpi-robot - Raspberry Pi Robot
Copyright (C) 2017  Blair Azzopardi
Distributed under the terms of the GNU General Public License (GPL v3)
'''
import os
import io
import base64

import numpy
from lxml import etree  # @UnresolvedImport
import aiohttp_xmlrpc.common
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

schema_path = os.path.join(os.path.dirname(aiohttp_xmlrpc.common.__file__), "xmlrpc.rng")
relaxng_doc = etree.parse(schema_path)
new_element = etree.fromstring('<element name="numpy.ndarray"><data type="base64Binary" /></element>')
relaxng_doc.xpath("/x:grammar/x:define[@name='value']/x:element/x:choice", namespaces={"x": "http://relaxng.org/ns/structure/1.0"})[0].append(new_element)
# todo: for some reason we need to freeze/thaw xml to/from string here
aiohttp_xmlrpc.common.schema = etree.RelaxNG(etree.fromstring(etree.tostring(relaxng_doc))) # etree.RelaxNG(relaxng_doc)

