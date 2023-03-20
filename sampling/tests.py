import unittest

from django.test import TestCase

# Create your tests here.
from sampling.SimpleRandom import SimpleRandom


class StateTestCase(TestCase):
    def test_state(self):
        self.assertEqual(1, 1)


class OptionTestCase(TestCase):
    def test_option(self):
        self.assertEqual(1, 1)


class DecisionTreeTestCase(TestCase):
    def test_decision_tree(self):
        self.assertEqual(1, 1)


class SimpleRandomTestCase(unittest.TestCase):

    def setUp(self):
        self.sr = SimpleRandom(5, 95, 100, 0, 0, None)

    def test_calculate_sample_size(self):
        sample_size = self.sr.calculate_sample_size(self.sr.population_size, self.sr.margin_of_error,
                                                    self.sr.confidence_level, self.sr.non_response_rate)
        self.assertEqual(sample_size, {'total': 80})

    def test_calculate_subgroup_sample_sizes(self):
        subgroups = [{'name': 'a', 'size': 100}, {'name': 'b', 'size': 200}]
        subgroup_sample_size = self.sr.calculate_subgroup_sample_sizes(self.sr.margin_of_error,
                                                                       self.sr.confidence_level,
                                                                       self.sr.non_response_rate,
                                                                       subgroups)
        self.assertEqual(subgroup_sample_size['a'], 80)
        self.assertEqual(subgroup_sample_size['b'], 132)

    def test_calculate_subgroup_sample_sizes_empty(self):
        subgroups = []
        subgroup_sample_size = self.sr.calculate_subgroup_sample_sizes(self.sr.margin_of_error,
                                                                       self.sr.confidence_level,
                                                                       self.sr.non_response_rate,
                                                                       subgroups)
        self.assertEqual(subgroup_sample_size, {})

    def test_calculate_subgroup_sample_sizes_single(self):
        subgroups = [{'name': 'a', 'size': 100}]
        subgroup_sample_size = self.sr.calculate_subgroup_sample_sizes(self.sr.margin_of_error,
                                                                       self.sr.confidence_level,
                                                                       self.sr.non_response_rate,
                                                                       subgroups)
        self.assertEqual(subgroup_sample_size['a'], 80)

    def test_sample_size_returns_correct_value_when_initialized(self):
        sr = SimpleRandom(margin_of_error=5, confidence_level=95, individuals=100, households=0, non_response_rate=0,
                          subgroups=None)
        sr.start_calculation()
        self.assertEqual(sr.get_sample_size(), {'total': 80})

    def test_non_response_rate_greater_than_100(self):
        simpleRandom = SimpleRandom(margin_of_error=5, confidence_level=95, individuals=100, households=0,
                                    non_response_rate=150, subgroups=None)
        with self.assertRaises(ValueError):
            simpleRandom.validate_inputs()

    def test_get_sample_size_raises_error_when_not_initialized(self):
        sr = SimpleRandom(5, 95, 100, 0, 0, None)
        with self.assertRaises(ValueError):
            sr.get_sample_size()

