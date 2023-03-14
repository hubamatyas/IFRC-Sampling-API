import math
import random

from sampling.SimpleRandom import SimpleRandom

time_slots = ['morning', 'evening']


class TimeLocation(SimpleRandom):
    def __init__(self, margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups,
                 locations, days):
        super().__init__(margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups)
        self.locations = locations
        self.days = days
        self.units = None

    def generate_time_location_combinations(self, locations, days):
        time_location_units = []
        for loc in range(1, locations + 1):
            for day in range(1, days + 1):
                for slot in time_slots:
                    time_location_units.append((loc, day, slot))
        return time_location_units

    def select_random_units(self, time_location_units):
        # Make sure that interviews_per_session is at least 10
        interviews_per_session = max(int(self.population_size / len(time_location_units)), 10)

        result = self.calculate_sample_size(self.population_size, self.margin_of_error, self.confidence_level,
                                                 self.non_response_rate)
        sample_size = result['total']

        # The total number of units to be selected
        num_units_to_select = int(sample_size / interviews_per_session)

        selected_subset = []
        while len(selected_subset) < num_units_to_select + 1:
            # Select a random subset of tuples
            selected_subset = random.sample(time_location_units, num_units_to_select)

            # Check if the sum of interviews per session is equal to the sample size
            interviews = sum([interviews_per_session for _ in selected_subset])
            if interviews == sample_size:
                return selected_subset
            elif interviews > sample_size:
                # If the sum of interviews exceeds the sample size, remove the last tuple from the selection
                excess = interviews - sample_size
                for _ in range(excess):
                    selected_subset.pop()
                return selected_subset
        # If the loop completes without selecting the required number of tuples, start the selection process again
        return self.select_random_units(self, time_location_units)

    def generate_desired_output(self, selected_subset):
        # Create a dictionary to store the output
        output_dict = {}

        # Loop through each tuple in the list
        for subset in selected_subset:
            location = f"Location{subset[0]}"
            day = f"Day{subset[1]}"
            time = subset[2]

            # Check if the location exists in the dictionary, if not add it
            if location not in output_dict:
                output_dict[location] = {}

            # Check if the day exists in the location dictionary, if not add it
            if day not in output_dict[location]:
                output_dict[location][day] = []

            # Add the time slot to the day list
            output_dict[location][day].append(time)

        # Convert the dictionary to the desired output format
        units = []
        for location in output_dict:
            location_dict = {location: []}
            for day in output_dict[location]:
                day_dict = {day: output_dict[location][day]}
                location_dict[location].append(day_dict)
            units.append(location_dict)
        self.units = units

    def start_calculation(self):
        time_location_units = self.generate_time_location_combinations(self.locations,self.days)
        selected_subset = self.select_random_units(time_location_units)
        self.generate_desired_output(selected_subset)

    def get_units(self):
        if self.units is None:
            raise ValueError("units are not initialized")
        return self.units





# if __name__ == '__main__':
#     timeLocation = TimeLocation(margin_of_error=5, confidence_level=95, individuals=100, households=0,
#                                 non_response_rate=0, subgroups=None,locations=3,days=5)
#     timeLocation.start_calculation()
#     result = timeLocation.get_units()
#     print(result)
