import unittest
import app.services
from model.puzzle import *


class TestServices(unittest.TestCase):
    def test_get_today(self):
        myservices = app.services.Services()
        today = myservices.get_today()
        assert today is None or isinstance(today, Clue)

    def test_get_yesterday(self):
        myservices = app.services.Services()
        yesterday = myservices.get_yesterday()
        assert yesterday is None or isinstance(yesterday, Puzzle)


if __name__ == '__main__':
    unittest.main()
