
from django.db import models
import math

#confidence interval
#margin of error
#population size
#sample size

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
    def __init__(self,margin_of_error,confidence_level,individuals,households,nonResponseRate,subgroups):
        self.margin_of_error = margin_of_error
        self.confidence_level = confidence_level
        self.individuals = individuals
        self.households = households
        self.nonResponseRate = nonResponseRate
        self.subgroups = subgroups

    def calculate_sample_size(self):
        confidence_interval = self.confidence_interval
        individuals = self.individuals
        margin_of_error = self.margin_of_error
        z = zscorecalculator(confidence_interval)
        numerator = (z * z * 0.5 * 0.5) / margin_of_error * margin_of_error
        denominator = 1 + (numerator / individuals)
        sample_size = numerator / denominator
        return math.ceil(sample_size)





