# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 29.10.2023

  Purpose: Class for creating and processes config files.
"""

import os
import sys
from inspect import currentframe
from typing import List, Dict, Tuple, Optional, Union, Any
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise
from jsktoolbox.libs.base_data import BData
from jsktoolbox.libs.system import PathChecker


class FileProcessor(BData, NoDynamicAttributes):
    """FileProcessor class."""

    def __init__(self) -> None:
        """Constructor."""

    @property
    def file(self) -> Optional[str]:
        """Return config file path."""
        if "file" not in self._data:
            self._data["file"] = None
        if isinstance(self._data["file"], PathChecker):
            return self._data["file"].path
        return self._data["file"]

    @file.setter
    def file(self, path: str) -> None:
        """Set file name."""
        self._data["file"] = PathChecker(path)

    @property
    def file_exists(self) -> bool:
        """Check if the file exists and is a file."""
        obj: PathChecker = self._data["file"]
        return (
            obj.exists and (obj.is_file or obj.is_symlink) and not obj.is_dir
        )

    def file_create(self) -> bool:
        """Try to create file."""
        if self.file_exists:
            return True
        obj: PathChecker = self._data["file"]
        if obj.exists and obj.is_dir:
            raise Raise.error(
                f"Given path: {obj.path} exists and is a directory.",
                OSError,
                self.__class__.__name__,
                currentframe(),
            )
        return obj.create()

    def read(self) -> str:
        """Try to read config file."""
        out = ""
        if self.file_exists:
            with open(self.file, "r") as file:
                out = file.read()
        return out

    def write(self, data: str) -> None:
        """Try to write data to config file."""
        test = self.file_exists
        if not test:
            test = self.file_create()
        if test:
            with open(self.file, "w") as file:
                file.write(data)


# #[EOF]#######################################################################
