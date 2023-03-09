import random


def generate_time_location_combinations(locations, days, time_slots):
    time_location_generator = []
    for loc in range(1, locations + 1):
        for day in range(1, days + 1):
            for slot in range(1, time_slots + 1):
                time_location_generator.append((loc, day, slot))
    return time_location_generator

# result = generate_time_location_combinations(locations = 3, days= 4, time_slots = 2)
# print(result)

def select_random_tuples(time_location_generator, sample_size, num_of_people_per_interview):
    # Make sure that num_of_people_per_interview is at least 10
    num_of_people_per_interview = max(num_of_people_per_interview, 10)

    selected_tuples = []
    while len(selected_tuples) < int(sample_size / num_of_people_per_interview):
        # Select a random subset of tuples
        selected_subset = random.sample(time_location_generator, int(sample_size / num_of_people_per_interview))

        # Check if the sum of interviews per session is equal to the sample size
        interviews = sum([num_of_people_per_interview for _ in selected_subset])
        if interviews == sample_size:
            return selected_subset
        elif interviews > sample_size:
            # If the sum of interviews exceeds the sample size, remove the last tuple from the selection
            excess = interviews - sample_size
            for _ in range(excess):
                selected_subset.pop()
            return selected_subset
    # If the loop completes without selecting the required number of tuples, start the selection process again
    return select_random_tuples(time_location_generator, sample_size, num_of_people_per_interview)

# city = "La Paz"
population = 100
num_locations = 3
num_days = 7
num_time_slots = 2
sample_size = 80
result = generate_time_location_combinations(locations=3, days=4, time_slots=2)
num_of_people_per_interview = int(population / len(result))
# print(num_of_people_per_interview)

target_per_location = int(sample_size / num_locations)
target_per_day = sample_size / num_days
target_survey = 80

if __name__=='__main__':
    selected_tuples = select_random_tuples(result, sample_size, num_of_people_per_interview)
    print(selected_tuples)
    print("(location,Day,Time_interval)")