from django.db import models
import math

PS = 0.5  # estimated proportion of successes
DF = 0.01  # Percentage to decimal factor


class SimpleRandom:
    def __init__(self, margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups):
        self.margin_of_error = float(margin_of_error)
        self.confidence_level = int(confidence_level)
        self.individuals = int(individuals) if individuals else None
        self.households = int(households) if households else None
        self.non_response_rate = float(non_response_rate) if non_response_rate else 0
        self.subgroups = subgroups
        self.sample_size = None
        if self.individuals or self.households:
            if self.individuals:
                self.population_size = self.individuals
            else:
                self.population_size = self.households * 4  # assumed the average number of people in a single
                # household = 4

    def validate_inputs(self):
        if self.margin_of_error is None:
            raise ValueError("margin_of_error cannot be None")
        if self.margin_of_error == 0:
            raise ValueError("margin_of_error cannot be zero")
        if self.margin_of_error < 0:
            raise ValueError("margin_of_error cannot be negative")
        if self.margin_of_error > 100:
            raise ValueError("margin_of_error cannot be greater than 100")
        if self.margin_of_error is not float:
            raise TypeError("margin_of_error can only be a number")

        if self.confidence_level is None:
            raise ValueError("confidence_level cannot be None")
        if self.confidence_level not in [99, 95, 90, 85, 80]:
            raise ValueError("confidence_level incorrect value raised")
        if self.confidence_level is not int:
            raise TypeError("confidence_level can only be a number")

        if self.non_response_rate is None:
            raise ValueError("non_response_rate cannot be None")
        if self.non_response_rate < 0:
            raise ValueError("non_response_rate cannot be negative")
        if self.non_response_rate > 100:
            raise ValueError("non_response_rate cannot be greater than 100")
        if self.non_response_rate is not float:
            raise TypeError("non_response_rate can only be a number")

        if self.individuals is not int:
            raise TypeError("number of individuals can only be a number")
        if self.households is not int:
            raise TypeError("number of households can only be a number")

    def start_calculation(self):
        self.validate_inputs()
        if self.subgroups is not None:
            self.sample_size = self.calculate_subgroup_sample_sizes(self.margin_of_error, self.confidence_level,
                                                                    self.non_response_rate, self.subgroups)

        else:
            self.sample_size = self.calculate_sample_size(self.population_size, self.margin_of_error,
                                                          self.confidence_level, self.non_response_rate)

    # https://www.surveymonkey.co.uk/mp/sample-size-calculator/
    def calculate_sample_size(self, population_size, margin_of_error, confidence_level, non_response_rate):

        z_scores = {
            80: 1.28,
            85: 1.44,
            90: 1.65,
            95: 1.96,
            99: 2.58
        }
        z = z_scores.get(confidence_level)
        numerator = (z * z * PS * PS) / (margin_of_error * margin_of_error * DF * DF)
        # print(numerator)
        denominator = 1 + (numerator / population_size)
        # print(denominator)
        ans = numerator / denominator
        sample_size = ans / (1 - (non_response_rate / 100))
        return math.ceil(sample_size)

    # Stratified Random Sampling
    def calculate_subgroup_sample_sizes(self, margin_of_error, confidence_level, non_response_rate,
                                        subgroups):
        subgroup_sample_size = {}
        # print(subgroups)
        # Format of subgroups : [{'name':'a','size':100},{'name':'b','size':200}]
        for subgroup in subgroups:
            # print(subgroup)
            ans = self.calculate_sample_size(subgroup['size'], margin_of_error, confidence_level, non_response_rate)
            subgroup_sample_size[subgroup['name']] = ans
        # cumulative_sample_size = sum(subgroup_sample_size.values())
        # Format of subgroup_sample_size = {'a':sample_size_a , 'b':sample_size_b}
        return subgroup_sample_size

    def get_sample_size(self):
        if self.sample_size is None:
            raise ValueError("sample_size not initialized")
        return self.sample_size


# if __name__ == '__main__':
#     simpleRandom = SimpleRandom(margin_of_error=5, confidence_level=95, individuals=100, households=0,
#                                 non_response_rate=0, subgroups=None)
#     # simple_random = SimpleRandom(0.05,95,100,0,5,0)
#     # print(simple_random)
#     simpleRandom.start_calculation()
#     sample_size = simpleRandom.get_sample_size()
#     print(sample_size)
