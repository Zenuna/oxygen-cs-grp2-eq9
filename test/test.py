import os
from unittest import TestCase, mock
import unittest

import src
from src import main
class MainTesting(TestCase):

    def setUp(self):
        self.app = main
        main.Main.__init__(main.Main)
    @mock.patch.dict(os.environ, {"HOST" : "", "TOKEN" : "None","TICKETS" : "0", "T_MAX" : "90", "T_MIN" : "10", "DATABASE" : "DB"})
    def test_env_default_value(self):
        assert os.getenv("HOST") == ""
        assert os.getenv("TOKEN") == "None"
        assert os.getenv("TICKETS") == "0"
        assert os.getenv("T_MAX") == "90"
        assert os.getenv("T_MIN") == "10"
        assert os.getenv("DATABASE") == 'DB'

    def test_env_set_value(self):
        assert self.app.Main.HOST == 'http://34.95.34.5'
        assert self.app.Main.TOKEN == 'Um9aQilWFM'
        assert self.app.Main.TICKETS == 1
        assert self.app.Main.T_MAX == 100
        assert self.app.Main.T_MIN == 0
        assert self.app.Main.DATABASE == 'sqlite:///C:\\dblabo.db'


if __name__ == '__main__':
    unittest.main()