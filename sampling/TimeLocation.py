
import math
from sampling.SimpleRandom import SimpleRandom

time_slots = ['morning','evening']

class TimeLocation(SimpleRandom):
    def __init__(self, margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups):
        super().__init__(margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups)
        self.locations = None
        self.days = None
        self.units = None

    def generate_time_location_combinations(self, locations,days):
        time_location_units = []
        for loc in range(1, locations + 1):
            for day in range(1, days + 1):
                for slot in time_slots:
                    time_location_units.append((loc, day, slot))
        return time_location_units

    def select_random_units(self,time_location_units):
        # Make sure that interviews_per_session is at least 10
        interviews_per_session = max(int(population / len(time_location_units)), 10)

        # The total number of units to be selected
        num_units_to_select = int(sample_size/interviews_per_session)

        sample_size = self.calculate_sample_size(self.population_size, self.margin_of_error, self.confidence_level, self.non_response_rate)

        while len(selected_tuples) < num_units_to_select+1:
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
        return select_random_tuples(self,time_location_units)

    def generate_desired_output(selected_subset):
        # Create a dictionary to store the output
        output_dict = {}

        # Loop through each tuple in the list
        for tuple in time_location_units:
            location = f"Location{tuple[0]}"
            day = f"Day{tuple[1]}"
            time = tuple[2]

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
        return units

    def get_units(self):
        if self.units is None:
            raise ValueError("units are not initialized")
        return self.units


