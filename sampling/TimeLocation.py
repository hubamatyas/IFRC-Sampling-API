import math
import random

from sampling.SimpleRandom import SimpleRandom

time_slots = ['morning', 'evening']


class TimeLocation(SimpleRandom):
    def __init__(self, margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups,
                 locations, days, interviews_per_session):
        super().__init__(margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups)
        self.locations = locations
        self.days = days
        self.interviews_per_session = max(interviews_per_session, 10)
        self.units = None

    def validate_inputs(self):
        result = self.calculate_sample_size(self.population_size, self.margin_of_error, self.confidence_level,
                                            self.non_response_rate)
        sample_size = result['total']
        if self.interviews_per_session > sample_size:
            raise ValueError("Interviews per session cannot be greater than sample size")

    def generate_time_location_combinations(self, locations, days):
        time_location_units = []
        for loc in range(1, locations + 1):
            for day in range(1, days + 1):
                for slot in time_slots:
                    time_location_units.append((loc, day, slot))
        return time_location_units

    def select_random_units(self, time_location_units):
        # Make sure that interviews_per_session is at least 10
        # interviews_per_session = max(int(self.population_size / len(time_location_units)), 10)

        result = self.calculate_sample_size(self.population_size, self.margin_of_error, self.confidence_level,
                                            self.non_response_rate)
        sample_size = result['total']
        # print("sample_size", sample_size)

        # The total number of units to be selected
        num_units_to_select = math.ceil(sample_size / self.interviews_per_session)
        # print("num_units_to_select", num_units_to_select)

        selected_subset = random.sample(time_location_units, num_units_to_select)
        # print("selected subset=", selected_subset)
        found_valid_selection = False
        while not found_valid_selection:

            # Check if the sum of interviews per session is equal to the sample size
            interviews = sum([self.interviews_per_session for _ in selected_subset])
            # print("interviews", interviews)
            if interviews == sample_size:
                found_valid_selection = True
            elif interviews > sample_size:
                # If the sum of interviews exceeds the sample size, remove the last tuple from the selection
                excess = interviews - sample_size
                if excess <= self.interviews_per_session:
                    selected_subset.pop()
                    found_valid_selection = True
                else:
                    number_units_to_delete = int(excess / self.interviews_per_session)
                    for i in range(number_units_to_delete):
                        selected_subset.pop()
                        found_valid_selection = True

        return selected_subset

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
        self.validate_inputs()
        time_location_units = self.generate_time_location_combinations(self.locations, self.days)
        selected_subset = self.select_random_units(time_location_units)
        self.generate_desired_output(selected_subset)

    def get_units(self):
        if self.units is None:
            raise ValueError("units are not initialized")
        return self.units


# if __name__ == '__main__':
#     timeLocation = TimeLocation(margin_of_error=5, confidence_level=95, individuals=500, households=0,
#                                 non_response_rate=0, subgroups=None, locations=5, days=8, interviews_per_session=20)
#     timeLocation.start_calculation()
#     result = timeLocation.get_units()
#     print(result)
