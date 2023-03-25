import math
import random

from sampling.SimpleRandom import SimpleRandom

time_slots = ['morning', 'evening']


class TimeLocation(SimpleRandom):
    def __init__(self, margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups,
                 locations, days, interviews_per_session):
        """
        A class for generating a sample of time-location units for a survey.
        Inherits from SimpleRandom class for calculating sample sizes.

        Parameters:
        Same as SimpleRandom with the following:

        locations (int): the number of locations to sample from
        days (int): the number of working days to sample
        interviews_per_session (int): the number of interviews per time-location unit session

        """

        super().__init__(margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups)
        self.locations = locations
        self.days = days
        self.interviews_per_session = max(interviews_per_session, 10)
        self.units = None

    def validate_inputs(self):
        """
            Validate that the inputs are valid and raise an error if not.
        """

        result = self.calculate_sample_size(self.population_size, self.margin_of_error, self.confidence_level,
                                            self.non_response_rate)
        sample_size = result['total']
        if self.interviews_per_session > sample_size:
            raise ValueError("Interviews per session cannot be greater than sample size")

    def generate_time_location_combinations(self, locations, days):
        """
            Generate all possible time-location combinations for the given number of locations and days.

            Parameters:
               locations (int): the number of locations to sample from
               days (int): the number of days to sample from

            Returns:
               time_location_units (list): a list of tuples representing all possible time-location combinations

        """

        time_location_units = []
        for loc in range(1, locations + 1):
            for day in range(1, days + 1):
                for slot in time_slots:
                    time_location_units.append((loc, day, slot))
        # print(time_location_units)
        return time_location_units

    def select_random_units(self, time_location_units):

        """
            Select a random subset of time-location units for the survey.

            Parameters:
                time_location_units (list): a list of tuples representing all possible time-location combinations

            Returns:
                selected_subset (list): a list of tuples representing the selected time-location units

        """

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

        # print(selected_subset)

        return selected_subset

    def generate_dict_of_selected_subset(self, selected_subset):

        # Create a dictionary to store the output
        output_dict = {}

        # Loop through each tuple in the list
        for subset in selected_subset:
            location = f"Location {subset[0]}"
            day = f"Day {subset[1]}"
            time = subset[2]

            # Check if the location exists in the dictionary, if not add it
            if location not in output_dict:
                output_dict[location] = {}

            # Check if the day exists in the location dictionary, if not add it
            if day not in output_dict[location]:
                output_dict[location][day] = []

            # Add the time slot to the day list
            output_dict[location][day].append(time)

        # print(output_dict)
        return output_dict

    def generate_desired_result(self,output_dict):
        # Convert the dictionary to the desired and sorted output format
        units = []
        for location in sorted(output_dict):
            location_dict = {location: []}
            for day in sorted(output_dict[location]):
                day_dict = {day: output_dict[location][day]}
                location_dict[location].append(day_dict)
            # Sort the days in each location
            location_dict[location] = sorted(location_dict[location], key=lambda x: list(x.keys())[0])
            units.append(location_dict)
        self.units = units
        # print(self.units)
        return units

    def start_calculation(self):
        self.validate_inputs()
        time_location_units = self.generate_time_location_combinations(self.locations, self.days)
        selected_subset = self.select_random_units(time_location_units)
        dict_format_of_selected_subset = self.generate_dict_of_selected_subset(selected_subset)
        units = self.generate_desired_result(dict_format_of_selected_subset)

    def get_units(self):
        if self.units is None:
            raise ValueError("units are not initialized")
        return self.units


if __name__ == '__main__':
    timeLocation = TimeLocation(margin_of_error=5, confidence_level=95, individuals=500, households=0,
                                non_response_rate=0, subgroups=None, locations=3, days=4, interviews_per_session=20)
    timeLocation.start_calculation()
    result = timeLocation.get_units()
    print(result)
