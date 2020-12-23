# -*- coding: utf-8 -*-
import logging
from xml.etree import ElementTree

_LOGGER = logging.getLogger(__name__)


class FritzhomeButton(object):
    """The Fritzhome Button class."""

    def __init__(self, node=None):
        if node is not None:
            self._update_from_node(node)

    def _update_from_node(self, node):
        _LOGGER.debug(ElementTree.tostring(node))
        self.ain = node.attrib["identifier"]
        self.identifier = node.attrib["id"]

        self.name = node.findtext("name")
        lastpressedtimestamp = node.findtext("lastpressedtimestamp")
        self.lastpressedtimestamp = int(
            lastpressedtimestamp) if lastpressedtimestamp else None
