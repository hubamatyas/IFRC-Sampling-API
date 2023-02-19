from django.db import models
import math


# confidence interval
# margin of error
# population size
# sample size

def zscorecalculator(ci):
    match ci:
        case 80:
            return 1.28
        case 85:
            return 1.44
        case 90:
            return 1.65
        case 95:
            return 1.96
        case 99:
            return 2.58


class SimpleRandom:
    def __init__(self, margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups):
        self.margin_of_error = margin_of_error
        self.confidence_level = confidence_level
        self.non_response_rate = non_response_rate
        self.subgroups = subgroups
        self.individuals = individuals
        self.households = households

        if individuals is not None:
            self.individuals = individuals
            self.population_size = individuals

        elif households is not None:
            self.households = households
            self.population_size = households * 4  # assumed the average number of people in a single household = 4

        else:
            raise ValueError("Either the number of individuals or the number of households must be specified")

        if subgroups is None:
            self.sample_size = self.calculate_sample_size(self.population_size, self.margin_of_error,
                                                          self.confidence_level, self.non_response_rate)
        else:
            self.sample_size = self.calculate_subgroup_sample_sizes(self.population_size, self.margin_of_error,
                                                                    self.confidence_level, self.non_response_rate,
                                                                    self.subgroups)

    def calculate_sample_size(self, population_size, margin_of_error, confidence_level, non_response_rate):

        z = zscorecalculator(confidence_level)
        numerator = (z * z * 0.5 * 0.5) / margin_of_error * margin_of_error
        denominator = 1 + (numerator / population_size)
        ans = numerator / denominator
        sample_size = ans/(1-(non_response_rate/100))
        return math.ceil(sample_size)

    # Stratified Random Sampling
    def calculate_subgroup_sample_sizes(self, population_size, margin_of_error, confidence_level, non_response_rate,
                                        subgroups):
        subgroup_sample_sizes = {}
        for subgroup, subgroup_size in subgroups.items():
            subgroup_sample_size = self.calculate_sample_size(subgroup_size, margin_of_error, confidence_level,
                                                              non_response_rate)
            subgroup_sample_sizes[subgroup] = int(subgroup_sample_size)
        sample_size = sum(subgroup_sample_sizes.values())
        return math.ceil(sample_size)

    def get_sample_size(self):
        return self.sample_size
