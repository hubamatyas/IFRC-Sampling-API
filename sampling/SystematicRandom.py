import math

from sampling.SimpleRandom import SimpleRandom


class SystematicRandom(SimpleRandom):
    def __init__(self, margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups):
        super().__init__(margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups)

    def get_result(self):
        print(self.sample_size)
        interval = math.ceil(self.population_size / self.sample_size)  # The step count
        # sample_size = math.ceil(self.population_size / interval)
        return interval


# if __name__ == '__main__':
#     systematicRandom = SystematicRandom(margin_of_error=5, confidence_level=95, individuals=100, households=110,
#                                         non_response_rate=5, subgroups=0)
#     result = systematicRandom.get_result()
#     print(result)
