from django.db import models
import math

PS = 0.5  # estimated proportion of successes
DF = 0.01  # Percentage to decimal factor

"""  

SimpleRandom is a sampling process that implements methods for calculating sample sizes based on various parameters. 
It serves as the parent class for the three other calculators. 

"""


class SimpleRandom:
    def __init__(self, margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups):

        """
        Initializes a SimpleRandom object with the given inputs.

        Parameters:
            margin_of_error (int): The maximum margin of error allowed for the sample.
            confidence_level (int): The confidence level for the sample, as a percentage.
            individuals (int): The number of individuals in the population, if applicable.
            households (int): The number of households in the population, if applicable.
            non_response_rate (int): The percentage of non-response rate expected for the sample.
            subgroups (list of dictionaries): A list of subgroups to be sampled from, with the following keys:
                - name: The name of the subgroup.
                - size: The size of the subgroup in the population.
                - Format of subgroups : [{'name':'SUBGROUP1','size':1000},{'name':'SUBGROUP2','size':2000}]

        Raises:
            TypeError: If any input is not of the correct type.
            ValueError: If any input is invalid.
        """

        self.check_inputs(margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups)
        self.margin_of_error = int(margin_of_error)
        self.confidence_level = int(confidence_level)
        self.individuals = int(individuals) if individuals else None
        self.households = int(households) if households else None
        self.non_response_rate = int(non_response_rate) if non_response_rate else 0
        self.subgroups = subgroups
        self.sample_size = None
        if self.individuals or self.households:
            if self.individuals:
                self.population_size = self.individuals
            else:
                self.population_size = self.households

    def check_inputs(self, margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups):
        if not isinstance(margin_of_error, int) and margin_of_error is not None:
            raise TypeError("margin_of_error can only be a number")
        if not isinstance(confidence_level, int) and confidence_level is not None:
            raise TypeError("confidence_level can only be a number")
        if not isinstance(individuals, int) and individuals is not None:
            raise TypeError("number of individuals can only be a number")
        if not isinstance(households, int) and households is not None:
            raise TypeError("number of households can only be a number")

    def validate_inputs(self):
        if self.margin_of_error is None:
            raise ValueError("margin_of_error cannot be None")
        if self.margin_of_error == 0:
            raise ValueError("margin_of_error cannot be zero")
        if self.margin_of_error < 0:
            raise ValueError("margin_of_error cannot be negative")
        if self.margin_of_error > 100:
            raise ValueError("margin_of_error cannot be greater than 100")

        if self.confidence_level is None:
            raise ValueError("confidence_level cannot be None")
        if self.confidence_level not in [99, 95, 90, 85, 80]:
            raise ValueError("confidence_level incorrect value raised")

        if self.non_response_rate is None:
            raise ValueError("non_response_rate cannot be None")
        if self.non_response_rate < 0:
            raise ValueError("non_response_rate cannot be negative")
        if self.non_response_rate > 100:
            raise ValueError("non_response_rate cannot be greater than 100")

    def start_calculation(self):
        self.validate_inputs()
        if self.subgroups is not None:
            self.sample_size = self.calculate_subgroup_sample_sizes(self.margin_of_error, self.confidence_level,
                                                                    self.non_response_rate, self.subgroups)

        else:
            self.sample_size = self.calculate_sample_size(self.population_size, self.margin_of_error,
                                                          self.confidence_level, self.non_response_rate)

    def calculate_sample_size(self, population_size, margin_of_error, confidence_level, non_response_rate):

        """
               Calculates the sample size for simple random sampling when there are no subgroups involved.
               It calculates the sample size of a single group or a community

        Formula to calculate the sample size derived from : https://www.surveymonkey.co.uk/mp/sample-size-calculator/

        Returns:
                A dictionary with the total sample size in the format {'total':sample_size}
        """

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
        return {"total": math.ceil(sample_size)}

    # Stratified Random Sampling
    def calculate_subgroup_sample_sizes(self, margin_of_error, confidence_level, non_response_rate,
                                        subgroups):
        """

    Calculates the sample sizes for each subgroup in a stratified random sampling method.

    Returns: A dictionary with the sample sizes for each subgroup.

    Format of subgroup_sample_size = { 'SUBGROUP1':sample_size_of_SUBGROUP1 ,'SUBGROUP2':sample_size_of_SUBGROUP2}

        """
        subgroup_sample_size = {}
        # print(subgroups)
        for subgroup in subgroups:
            # print(subgroup)
            ans = self.calculate_sample_size(subgroup['size'], margin_of_error, confidence_level, non_response_rate)
            subgroup_sample_size[subgroup['name']] = ans['total']
        return subgroup_sample_size

    def get_sample_size(self):

        """  Returns the sample size. """

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
