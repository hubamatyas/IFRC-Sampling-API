import os
import unittest
import xmlrunner
import xml.etree.ElementTree as ET
from django.test import TestCase
import unittest
import coverage
from sampling import *
from sampling.ClusterRandom import ClusterRandom
from sampling.SystematicRandom import SystematicRandom
from sampling.TimeLocation import TimeLocation
from sampling.SimpleRandom import SimpleRandom
from django.conf import settings

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

import sys

# Add the parent directory of the current file to the Python path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Add the directory containing the `myproject` module to the Python path
myproject_dir = os.path.abspath(os.path.join(parent_dir, 'myproject'))
if myproject_dir not in sys.path:
    sys.path.insert(0, myproject_dir)

cov = coverage.Coverage(source=['sampling'])
cov.start()

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


class SystematicRandomTestCase(unittest.TestCase):
    def setUp(self):
        self.individuals = 100
        self.households = 0
        self.non_response_rate = 5
        self.subgroups = [{'name': 'a', 'size': 50}, {'name': 'b', 'size': 50}]
        self.margin_of_error = 5
        self.confidence_level = 95

    def test_start_calculation_no_subgroups(self):
        systematic_random = SystematicRandom(self.margin_of_error, self.confidence_level, self.individuals,
                                             self.households, self.non_response_rate, None)
        systematic_random.start_calculation()
        self.assertEqual(systematic_random.get_intervals(), {'total': 2})

    def test_start_calculation_with_subgroups(self):
        systematic_random = SystematicRandom(self.margin_of_error, self.confidence_level, self.individuals,
                                             self.households, self.non_response_rate, self.subgroups)
        systematic_random.start_calculation()
        self.assertEqual(systematic_random.get_intervals(), {'a': 2, 'b': 2})

    def test_get_intervals_before_start_calculation(self):
        systematic_random = SystematicRandom(self.margin_of_error, self.confidence_level, self.individuals,
                                             self.households, self.non_response_rate, self.subgroups)
        with self.assertRaises(ValueError):
            systematic_random.get_intervals()

    def test_get_intervals_after_start_calculation(self):
        systematic_random = SystematicRandom(self.margin_of_error, self.confidence_level, self.individuals,
                                             self.households, self.non_response_rate, self.subgroups)
        systematic_random.start_calculation()
        self.assertIsNotNone(systematic_random.get_intervals())

    def test_get_intervals_type(self):
        systematic_random = SystematicRandom(self.margin_of_error, self.confidence_level, self.individuals,
                                             self.households, self.non_response_rate, self.subgroups)
        systematic_random.start_calculation()
        intervals = systematic_random.get_intervals()
        self.assertIsInstance(intervals, dict)
        for key in intervals:
            self.assertIsInstance(intervals[key], int)


class TimeLocationTestCase(unittest.TestCase):

    def setUp(self):
        self.margin_of_error = 5
        self.confidence_level = 95
        self.individuals = 100
        self.sample_size = 80
        self.households = 0
        self.non_response_rate = 0
        self.subgroups = None
        self.locations = 3
        self.days = 4
        self.interviews_per_session = 20
        self.time_location = TimeLocation(self.margin_of_error, self.confidence_level, self.individuals,
                                          self.households, self.non_response_rate, self.subgroups, self.locations,
                                          self.days, self.interviews_per_session)

    def test_if_total_interviews_equals_sample_size_in_select_random_units(self):
        self.time_location.interviews_per_session = 10
        result = self.time_location.generate_time_location_combinations(self.locations, self.days)
        random_units = self.time_location.select_random_units(result)
        self.assertEqual(len(random_units) * self.time_location.interviews_per_session, 80)

    def test_if_total_interviews_greater_than_sample_size_in_select_random_units(self):
        self.time_location.interviews_per_session = 40
        result = self.time_location.generate_time_location_combinations(self.locations, self.days)
        random_units = self.time_location.select_random_units(result)
        self.assertEqual(len(random_units), 2)

    def test_if_excess_less_than_interviews_per_session_in_select_random_units(self):
        self.time_location.interviews_per_session = 10
        result = self.time_location.generate_time_location_combinations(self.locations, self.days)
        random_units = self.time_location.select_random_units(result)
        self.assertEqual(len(random_units), 8)

    def test_generate_time_location_combinations(self):
        expected_output = [(1, 1, 'morning'), (1, 1, 'evening'), (1, 2, 'morning'), (1, 2, 'evening'),
                           (1, 3, 'morning'),
                           (1, 3, 'evening'), (1, 4, 'morning'), (1, 4, 'evening'), (2, 1, 'morning'),
                           (2, 1, 'evening'),
                           (2, 2, 'morning'), (2, 2, 'evening'), (2, 3, 'morning'), (2, 3, 'evening'),
                           (2, 4, 'morning'),
                           (2, 4, 'evening'), (3, 1, 'morning'), (3, 1, 'evening'), (3, 2, 'morning'),
                           (3, 2, 'evening'),
                           (3, 3, 'morning'), (3, 3, 'evening'), (3, 4, 'morning'), (3, 4, 'evening')]

        result = self.time_location.generate_time_location_combinations(self.locations, self.days)
        self.assertEqual(result, expected_output)

    def test_select_correct_number_of_random_units(self):
        time_location_units = self.time_location.generate_time_location_combinations(self.locations, self.days)
        selected_subset = self.time_location.select_random_units(time_location_units)
        expected_length = self.sample_size / self.interviews_per_session
        self.assertEqual(len(selected_subset), expected_length)


class ClusterRandomTestCase(unittest.TestCase):

    def setUp(self):
        self.margin_of_error = 5
        self.confidence_level = 95
        self.individuals = 100
        self.sample_size = 80
        self.households = 0
        self.non_response_rate = 0
        self.subgroups = None
        self.communities = [{'name': 'Community A', 'size': 1000}, {'name': 'Community B', 'size': 1500},
                            {'name': 'Community C', 'size': 2000}]
        self.community_sample_sizes = {'Community A': 278, 'Community B': 306, 'Community C': 323}
        self.cluster_random = ClusterRandom(self.margin_of_error, self.confidence_level, self.individuals,
                                            self.households, self.non_response_rate, self.subgroups, self.communities)

    def test_community_sample_size_calculation(self):
        # expected_output is calculated using a sample size calculator on surveymonkeys.com
        expected_output = {'Community A': 278, 'Community B': 306, 'Community C': 323}
        calculated_output = self.cluster_random.community_sample_sizes_calculation()
        self.assertEqual(expected_output, calculated_output)

    def test_assigned_clusters_greater_than_zero(self):
        calculated_output = self.cluster_random.assign_number_of_clusters(self.communities, self.community_sample_sizes,
                                                                          total_clusters=30)
        for community in calculated_output:
            self.assertGreaterEqual(calculated_output[community], 0)

    def test_number_of_assigned_clusters_equal_to_total_clusters(self):
        calculated_output = self.cluster_random.assign_number_of_clusters(self.communities, self.community_sample_sizes,
                                                                          total_clusters=30)
        assigned_clusters = sum(calculated_output.values())
        self.assertEqual(assigned_clusters, 30)

    def test_assign_list_of_clusters(self):
        # The following argument is not possible as the sample sizes are nearly the same and the number of clusters will
        # also be nearly balanced, that is, the number of clusters assigned to each community would be nearly equal

        calculated_output = self.cluster_random.assign_list_of_clusters(
            {'Community A': 20, 'Community B': 5, 'Community C': 5})

        expected_output = {'Community A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                           'Community B': [21, 22, 23, 24, 25],
                           'Community C': [26, 27, 28, 29, 30]}

        # Checks whether the function standalone is working correctly
        self.assertEqual(calculated_output, expected_output)

    def test_get_clusters_without_initialized_clusters(self):
        with self.assertRaises(ValueError):
            self.cluster_random.get_clusters()

    def test_total_assigned_clusters_equals_total_clusters(self):
        total_clusters = 3
        community_clusters = self.cluster_random.assign_number_of_clusters(self.communities,
                                                                           self.community_sample_sizes, total_clusters)
        self.assertEqual(sum(community_clusters.values()), total_clusters)

    def test_total_assigned_clusters_greater_than_total_clusters(self):
        total_clusters = 32
        community_clusters = self.cluster_random.assign_number_of_clusters(self.communities,
                                                                           self.community_sample_sizes, total_clusters)
        self.assertEqual(sum(community_clusters.values()), total_clusters)
        for name in community_clusters:
            self.assertTrue(1 <= community_clusters[name] <= 24)

    def test_total_assigned_clusters_less_than_total_clusters(self):
        total_clusters = 29
        community_clusters = self.cluster_random.assign_number_of_clusters(self.communities,
                                                                           self.community_sample_sizes, total_clusters)
        self.assertEqual(sum(community_clusters.values()), total_clusters)
        for name in community_clusters:
            self.assertTrue(1 <= community_clusters[name] <= 24)


print("Starting test suite...")
if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False)

cov.stop()
cov.save()
cov.report()