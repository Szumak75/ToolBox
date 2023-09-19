# -*- coding: UTF-8 -*-
"""
  Author:  Jacek Kotlarski --<szumak@virthost.pl>
  Created: 14.09.2023

  Purpose:
"""

from inspect import currentframe
from typing import Union, TypeVar
from jsktoolbox.attribtool import NoDynamicAttributes
from jsktoolbox.raisetool import Raise

from jsktoolbox.libs.interfaces.comparators import IComparators

TWord16 = TypeVar("TWord16", bound="Word16")


class Word16(IComparators, NoDynamicAttributes):
    """Class for representing ipv6 16-bits word.

    Constructor arguments:
    value [str|int|Octet] -- Value of word in proper range from 0x0000 to 0xffff

    Public property:
    value [int] -- Return integer representation of word.

    Public setters:
    value [str|int|Octet] -- Set value of word."""

    __value: int = 0

    def __init__(self, value: Union[str, int, TWord16]) -> None:
        """Constructor."""
        self.value = value

    def __eq__(self, arg: TWord16) -> bool:
        """Equal."""
        return self.value == arg.value

    def __ge__(self, arg: TWord16) -> bool:
        """Greater then or equal."""
        return self.value >= arg.value

    def __gt__(self, arg: TWord16) -> bool:
        """Greater then."""
        return self.value > arg.value

    def __le__(self, arg: TWord16) -> bool:
        """Less then or equal."""
        return self.value <= arg.value

    def __lt__(self, arg: TWord16) -> bool:
        """Less then."""
        return self.value < arg.value

    def __ne__(self, arg: TWord16) -> bool:
        """Negative."""
        return self.value != arg.value

    def __int__(self) -> int:
        """Return integer representation of word."""
        return self.value

    def __str__(self) -> str:
        """Return a hexadecimal string representing a word without the leading '0x'."""
        return hex(self.value)[2:]

    def __repr__(self):
        """Return representation of object."""
        return f"Word16({self.value})"

    @staticmethod
    def __check_range(value: int) -> bool:
        if value not in range(0, 65536):
            return False
        return True

    @staticmethod
    def __is_integer(value: str) -> bool:
        try:
            if value.find("0x") == 0:
                int(value, 16)
            else:
                int(value)
            return True
        except:
            return False

    @property
    def value(self) -> int:
        """Rerutn value of Word16 as int."""
        return self.__value

    @value.setter
    def value(
        self,
        args: Union[str, int, TWord16],
    ) -> None:
        if isinstance(args, int):
            if Word16.__check_range(args):
                self.__value = args
                return
            else:
                raise Raise.error(
                    f"Received value '{args}' out of range(0-65535).",
                    ValueError,
                )
        elif isinstance(args, str):
            if Word16.__is_integer(args):
                if args.find("0x") == 0:
                    var = int(args, 16)
                else:
                    var = int(args)
                if Word16.__check_range(var):
                    self.__value = var
                    return
                else:
                    raise Raise.error(
                        f"Received value '{args}' out of range(0-65535).",
                        ValueError,
                    )
        elif isinstance(args, Word16):
            tmp: TWord16 = args
            self.__value = tmp.value
            return
        raise Raise.error(
            f"Integer or String expected, {type(args)} received.",
            TypeError,
            self.__class__.__name__,
            currentframe(),
        )


# #[EOF]#######################################################################
