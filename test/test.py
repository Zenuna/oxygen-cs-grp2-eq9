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
        assert self.app.Main.HOST == 'GITHUB'
        assert self.app.Main.TOKEN == 'YES'
        assert self.app.Main.TICKETS == "100"
        assert self.app.Main.T_MAX == "100"
        assert self.app.Main.T_MIN == "100"
        assert self.app.Main.DATABASE == 'DBENV'

if __name__ == '__main__':
    unittest.main()