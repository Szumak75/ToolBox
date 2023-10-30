# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 29.10.2023

  Purpose: ConfigTool testing class.
"""

import unittest
from jsktoolbox.configtool.main import Config
from jsktoolbox.configtool.libs.file import FileProcessor


class TestConfig(unittest.TestCase):
    """ConfigTool testing class."""

    def setUp(self) -> None:
        """Set up test engine."""
        self.filename = "/tmp/configtool/a/b/c/d/e/test.conf"
        self.conf_template = """# This is example config file for test purpose only.
[first]
# section 'first'
name = "tests"
enable = yes
list = [10, 20, 30]
level = 7 # value of level
# example section comments nr 01
# example section comments nr 02
# :::::<End of section: 'first'>:::::

[second]
# section 'second'
value = 18k
label=
# :::::<End of section: 'second'>:::::

"""
        # create config file
        try:
            fp = FileProcessor()
            fp.file = self.filename
            if fp.file_create():
                fp.write(self.conf_template)
        except Exception as ex:
            self.fail(msg=f"{ex}")

    def test_01_create_object(self):
        """Test nr 01."""
        file: str = "/tmp/test/config.01.ini"
        sname: str = "TEST"
        try:
            Config(file, sname)
        except Exception:
            self.fail("somenting is very wrong.")

    def test_02_config_read(self):
        """Test nr 02."""
        obj = None
        try:
            obj = Config(self.filename, "configtool")
            # config file was created in setUp
            self.assertTrue(obj.file_exists)
            # load config
            self.assertTrue(obj.load())
            # save config
            self.assertTrue(obj.save())
        except Exception as ex:
            self.fail(msg=f"{ex}")


# #[EOF]#######################################################################
