import math

from sampling.SimpleRandom import SimpleRandom


class SystematicRandom(SimpleRandom):
    def __init__(self, margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups):
        super().__init__(margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups)

    def get_result(self):
        if self.subgroups is None:
            # print(self.sample_size)
            interval = math.ceil(self.population_size / self.sample_size)  # The step count
            # sample_size = math.ceil(self.population_size / interval)
            return interval
        else:
            interval = self.get_result_subgroups(self)
            return interval

    def get_result_subgroups(self):
        intervals = []
        for subgroup in self.subgroups:
            subgroup_size = subgroup['size']
            subgroup_sample_size = self.calculate_sample_size(subgroup_size, self.margin_of_error,
                                                              self.confidence_level, self.non_response_rate)
            subgroup_interval = math.ceil(subgroup_size / subgroup_sample_size)
            intervals.append(subgroup_interval)
        # will return a list with the value of each of the subgroup
        # [3,4] -> skip of subgroup_1 , skip of subgroup_2
        return intervals

# if __name__ == '__main__':
#     systematicRandom = SystematicRandom(margin_of_error=5, confidence_level=95, individuals=100, households=0,
#                                         non_response_rate=5, subgroups=0)
#     result = systematicRandom.get_result()
#     print("answer=", result)
