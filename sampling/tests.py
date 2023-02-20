from django.test import TestCase

# Create your tests here.
class StateTestCase(TestCase):
    def test_state(self):
        self.assertEqual(1, 1)

class OptionTestCase(TestCase):
    def test_option(self):
        self.assertEqual(1, 1)

class DecisionTreeTestCase(TestCase):
    def test_decision_tree(self):
        self.assertEqual(1, 1)