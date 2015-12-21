import unittest

from headspring import *

class TestHeadspringTools(unittest.TestCase):

    def test_generate_id(self):
        id_map = generate_id()
        self.assertIn("id", id_map.keys())