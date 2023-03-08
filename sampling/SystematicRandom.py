import math
from sampling.SimpleRandom import SimpleRandom


class SystematicRandom(SimpleRandom):
    def __init__(self, margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups):
        super().__init__(margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups)
        self.intervals = None

    def start_calculation(self):
        if self.subgroups is None:
            sample_size = self.calculate_sample_size(self.population_size, self.margin_of_error, self.confidence_level, self.non_response_rate)
            interval = math.ceil(self.population_size / sample_size['total'])  # The step count
            self.intervals = {'total': interval}
        else:
            self.intervals = {}
            for subgroup in self.subgroups:
                subgroup_size = subgroup['size']
                subgroup_sample_size = self.calculate_sample_size(subgroup_size, self.margin_of_error,
                                                                  self.confidence_level, self.non_response_rate)
                subgroup_interval = math.ceil(subgroup_size / subgroup_sample_size['total'])
                # Format of subgroups : [{'name':'a','size':100},{'name':'b','size':200}]
                self.intervals[subgroup['name']] = subgroup_interval

    def get_intervals(self):
        if self.intervals is None:
            raise ValueError("intervals not initialized")
        return self.intervals

# if __name__ == '__main__':
#     systematicRandom = SystematicRandom(margin_of_error=5, confidence_level=95, individuals=100, households=0,
#                                         non_response_rate=5, subgroups=None)
#     systematicRandom.start_calculation()
#     intervals = systematicRandom.get_calculation()
#     print("answer=", sample_size)
