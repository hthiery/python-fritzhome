"""The trigger class."""

from __future__ import annotations

import logging

from xml.etree import ElementTree

from .fritzhomeentitybase import FritzhomeEntityBase

_LOGGER = logging.getLogger(__name__)


class FritzhomeTrigger(FritzhomeEntityBase):
    """The Fritzhome Trigger class."""

    active: bool | None = None

    def _update_from_node(self, node: ElementTree.Element) -> None:
        _LOGGER.debug("update trigger")
        _LOGGER.debug(ElementTree.tostring(node))
        self.ain = node.attrib["identifier"]
        self.name = node.findtext("name", "").strip()
        self.active = node.attrib["active"] == "1"
