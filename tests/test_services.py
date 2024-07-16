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

    def test_submit(self):
        test_date = "2000/01/01"
        test_name = "Wilbur Wildcat"
        test_artist = "Rick Astley"
        test_title = "Never Gonna Give You Up"
        test_sub = Submission(test_name, test_date, test_title, test_artist)
        myservices = app.services.Services()
        response = myservices.record_submission(test_sub)
        assert response is True


if __name__ == '__main__':
    unittest.main()
