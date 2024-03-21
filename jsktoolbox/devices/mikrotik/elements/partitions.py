# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 08.12.2023

  Purpose: RB '/partitions/'
"""


from typing import Optional, Dict, Any

from jsktoolbox.attribtool import ReadOnlyClass
from jsktoolbox.logstool.logs import LoggerClient, LoggerQueue


from jsktoolbox.devices.mikrotik.base import BRouterOS, BDev
from jsktoolbox.devices.network.connectors import IConnector


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """


class _Elements(object, metaclass=ReadOnlyClass):
    """Keys definition class.

    For internal purpose only.
    """

    ROOT: str = "partitions"


class RBPartitions(BRouterOS):
    """Radius class

    For command root: /partitions/
    """

    def __init__(
        self,
        parent: BDev,
        connector: IConnector,
        qlog: Optional[LoggerQueue] = None,
        debug: bool = False,
        verbose: bool = False,
    ) -> None:
        """Constructor."""
        super().__init__(
            parent,
            connector,
            LoggerClient(queue=qlog, name=self._c_name),
            debug,
            verbose,
        )
        self.root = f"{_Elements.ROOT}/"

        # add elements
        elements: Dict[str, Any] = {}

        # configure elements
        self._add_elements(self, elements)


# #[EOF]#######################################################################
