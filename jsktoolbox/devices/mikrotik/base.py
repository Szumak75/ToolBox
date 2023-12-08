# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 04.12.2023

  Purpose: Base classes for RouterOS
"""

from typing import Dict, List, Optional, Union, Tuple, Any, TypeVar
from inspect import currentframe

from jsktoolbox.attribtool import NoDynamicAttributes, ReadOnlyClass
from jsktoolbox.raisetool import Raise
from jsktoolbox.logstool.logs import LoggerClient, LoggerQueue


from jsktoolbox.netaddresstool.ipv4 import (
    Address,
    Netmask,
    Network,
    SubNetwork,
)
from jsktoolbox.netaddresstool.ipv6 import (
    Address6,
    Network6,
    Prefix6,
    SubNetwork6,
)

from jsktoolbox.devices.mikrotik.elements.libs.interfaces import IElement
from jsktoolbox.devices.mikrotik.elements.libs.base import BElement
from jsktoolbox.devices.libs.base import BDev
from jsktoolbox.devices.network.connectors import IConnector, API, SSH

TRouterOs = TypeVar("TRouterOs", bound="BRouterOs")
TElement = TypeVar("TElement", bound="Element")


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    ELEMENTS = "__elements__"
    LOADED = "__loaded__"


class BRouterOS(BDev, BElement):
    """Base class for RouterOS."""

    def __init__(
        self,
        parent: BDev,
        connector: IConnector,
        logs: LoggerClient,
        debug: bool,
        verbose: bool,
    ) -> None:
        """Constructor."""
        self.parent = parent
        self._ch = connector
        self.logs = logs
        self.debug = debug
        self.verbose = verbose
        self._data[_Keys.LOADED] = False

    def __str__(self) -> str:
        """Returns a string representing the object."""
        return f"{self._c_name}(path='{self.root}', elements='{self.elements}', attrib='{self.attrib}', list='{self.list}')"

    def _add_elements(self, parent: TRouterOs, elements_dict: Dict) -> None:
        """Add childs from configuration dict."""
        for key in elements_dict.keys():
            if key in self.elements:
                # duplicate
                if self.debug:
                    self.logs.message_debug = f'duplicate key found: "{key}"'
                    continue
            obj = Element(
                key=key,
                parent=parent,
                connector=parent._ch,
                qlog=parent.logs.logs_queue,
                debug=parent.debug,
                verbose=parent.verbose,
            )
            self.elements[key] = obj
            if elements_dict[key]:
                obj._add_elements(obj, elements_dict[key])

    def dump(self):
        """Dump all dataset."""
        print(self.root)
        self.load(self.root)
        if self.attrib:
            print(f"attrib: {self.attrib}")
        if self.list:
            # print(f"list: {self.list}")
            for item in self.list:
                print(f"list: {item}")
        for item in self.elements.values():
            item.dump()

    def element(
        self, root: str, auto_load: bool = False
    ) -> Optional[TElement]:
        """Returns the Element object for corresponding path."""
        # check if first and last char in path is '/'
        if root:
            if root[0] != "/":
                root = f"/{root}"
            if root[-1:] != "/":
                root = f"{root}/"
        for key in self.elements.keys():
            element: Element = self.elements[key]
            if element.root == root:
                if auto_load:
                    element.load(root)
                return element
            element2: Element = element.element(root, auto_load)
            if element2 is not None:
                return element2
        return None

    @property
    def elements(self) -> Dict:
        """Return elements dict."""
        if _Keys.ELEMENTS not in self._data:
            self._data[_Keys.ELEMENTS] = {}
        return self._data[_Keys.ELEMENTS]

    def get(self) -> bool:
        """Gets config for current element."""
        return self.load(self.root)

    @property
    def is_loaded(self) -> bool:
        """Returns True if loaded."""
        return self._data[_Keys.LOADED]

    def load(self, root: str) -> bool:
        """Gets element config from RB."""
        if root is not None and not self._data[_Keys.LOADED]:
            ret = self._ch.execute(f"{root}print")
            if ret:
                out, err = self._ch.outputs()
                if (
                    out[0]
                    and isinstance(out[0], List)
                    and len(out[0]) == 1
                    and isinstance(out[0][0], Dict)
                ):
                    self.attrib.update(out[0][0])
                    self._data[_Keys.LOADED] = True
                elif (
                    out[0]
                    and isinstance(out[0], List)
                    and len(out[0]) > 1
                    and isinstance(out[0][0], Dict)
                ):
                    for item in out[0]:
                        self.list.append(item)
                    self._data[_Keys.LOADED] = True
                else:
                    if out[0]:
                        print(f"DEBUG_: {out}")
                if err[0]:
                    self.logs.message_warning = f"{out[0][0]}"
                    return False
                return True
        return False


class Element(BRouterOS):
    """MiktoTik Element class."""

    def __init__(
        self,
        key: str,
        parent: BDev,
        connector: IConnector,
        qlog: LoggerQueue = None,
        debug: bool = False,
        verbose: bool = False,
    ):
        """Constructor."""
        super().__init__(
            parent,
            connector,
            LoggerClient(queue=qlog, name=key),
            debug,
            verbose,
        )
        self.root = f"{key}/"

    def search(self, search_dict: Dict) -> Optional[Union[List, Dict]]:
        """Returns optional Dict or List[Dict] with found results."""
        # search_dict = {
        # key1: value1,
        # key2: None,
        # }
        if self.attrib:
            test = True
            for key, value in search_dict.items():
                if value:
                    if key in self.attrib and self.attrib[key] != value:
                        test = False
                elif key not in self.attrib:
                    test = False
            if test:
                return self.attrib
            return None

        if self.list:
            out = []
            for item in self.list:
                test = True
                for key, value in search_dict.items():
                    if value:
                        if key in item and item[key] != value:
                            test = False
                    elif key not in item:
                        test = False
                if test:
                    out.append(item)
            if out:
                return out

        return None


# #[EOF]#######################################################################
