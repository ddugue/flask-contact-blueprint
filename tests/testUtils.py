import unittest

from flask_contact.utils import AllowedList

class AllowedListTest(unittest.TestCase):
    """ Test case for the AllowedList class """
    def test_allowed_none(self):
        "Ensures that when no items are allowed it return False"
        self.assertFalse('' in AllowedList(None))
        self.assertFalse('' in AllowedList(''))
        self.assertFalse('' in AllowedList([]))

    def test_allowed_all(self):
        "Ensures that when all items are allowed it return True"
        self.assertTrue('' in AllowedList('*'))
        self.assertTrue('a' in AllowedList('*'))
        self.assertTrue(1 in AllowedList('*'))

    def test_allowed_single_string(self):
        "Ensures that when filtering for a single string it works"
        self.assertTrue('a' in AllowedList('a'))
        self.assertFalse('b' in AllowedList('a'))

    def test_allowed_some_string(self):
        "Ensures that when some items are allowed it works"
        self.assertTrue('a' in AllowedList('a b'))
        self.assertTrue('b' in AllowedList('a b'))
        self.assertFalse('c' in AllowedList('a b'))
        self.assertFalse('' in AllowedList('a b'))

    def test_filter_list(self):
        "Ensure that the filter work on a list"
        self.assertEqual(['a'], list(AllowedList('a').filter(['b', 'a', 'c'])))

    def test_filter_dict(self):
        "Ensure that the filter work on a list"
        allowed = AllowedList('a').filter({'a': 'b', 'c': 'd'})
        self.assertEqual([('a', 'b')], list(allowed))
