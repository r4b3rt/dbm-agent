# -*- coding: utf8 -*-

import unittest
from unittest.mock import Mock, patch, MagicMock, call, mock_open
from pathlib import Path

from dbma.components.mysql.config import (
    MySQLSystemdConfig,
    MySQLSRConfig,
)


class MySQLSystemdConfigTestCase(unittest.TestCase):
    """ """

    port = 3306
    basedir = "/usr/local/mysql-8.0.33-linux-glibc2.28-x86_64"

    def test_user_given_port_3306(self):
        """
        given: 给定 MySQL 的端口是 3306
        when: 创建 MySQLSystemdConfig 对象
        then: 对象的 user属性应该是 mysql3306
        """
        syscnf = MySQLSystemdConfig(port=self.port, basedir=self.basedir)
        self.assertEqual("mysql3306", syscnf.user)

    @patch.object(Path, "exists")
    def test_load_given_port_3306(self, mock_exists):
        """"""
        mock_exists.return_value = True
        with patch("dbma.core.configs.open", mock_open(read_data="x")) as mock:
            syscnf = MySQLSystemdConfig(port=self.port, basedir=self.basedir)
            syscnf.load()
            # open, enter, read, exit 共四个调用
            self.assertEqual(len(mock.mock_calls), 4)
            self.assertEqual(mock.mock_calls[2], call().read())

    @patch.object(Path, "exists")
    def test_load_given_template_file_not_exists(self, mock_exists):
        """"""
        mock_exists.return_value = False
        with self.assertRaises(ValueError):
            syscnf = MySQLSystemdConfig(port=self.port, basedir=self.basedir)
            syscnf.load()

    def test_render_given_port_3306(self):
        """ """
        with patch.object(MySQLSystemdConfig, "load") as mock:
            mock.return_value = "{{user}}\n"
            syscnf = MySQLSystemdConfig(self.port, self.basedir)
            expected = "mysql3306\n"
            self.assertEqual(expected, syscnf.render())


class MySQLSRConfigTestCase(unittest.TestCase):
    """ """

    port = 3306
    basedir = "/usr/local/mysql-8.0.33-linux-glibc2.28-x86_64"

    def test_config_template_path_given_port_3306(self):
        """ """
        cnf = MySQLSRConfig(3306, "/usr/local/mysql-8.0.33/", "128M")
        self.assertEqual(cnf.user, "mysql3306")
