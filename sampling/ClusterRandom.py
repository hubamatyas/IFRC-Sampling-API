import math
import random

from sampling.SimpleRandom import SimpleRandom

total_clusters = 30
max_clusters_per_location = 0.8 * 30

data_display = "The results for the sampling plan indicate they are not practical for implementation. This can " \
               "happen when there are large variances in population across geographical units. It is suggested to " \
               "instead use a simple or systematic random sampling approach for each geographical unit separately, " \
               "depending on whether or not you have an existing list frame. The results will not be representative " \
               "across the entire population, but will be representative for each geographical unit on its own."


class ClusterRandom(SimpleRandom):
    def __init__(self, margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups,
                 communities):
        super().__init__(margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups)
        self.communities = communities
        self.population_size = 0
        for community in communities:
            self.population_size += community['size']
        self.clusters = None

    def community_sample_sizes_calculation(self):
        """
                Calculate the sample size for each community.

                Returns:
                community_sample_sizes (dict): A dictionary containing the calculated sample size for each community.

        """
        community_sample_sizes = {}

        for community in self.communities:
            result = self.calculate_sample_size(community['size'], self.margin_of_error,
                                                self.confidence_level,
                                                self.non_response_rate)
            sample_size = result['total']
            community_sample_sizes[community['name']] = sample_size

        # print(community_sample_sizes)
        return community_sample_sizes

    def assign_number_of_clusters(self, communities, community_sample_sizes,total_clusters):

        """
                Assign the number of clusters for each community.

                Args:
                communities (list): A list of communities in the population, along with their sizes.
                community_sample_sizes (dict): A dictionary containing the calculated sample size for each community.
                total_clusters (int): The total number of clusters to assign.

                Returns:
                community_clusters (dict): A dictionary containing the assigned number of clusters for each community.
        """

        total_sample_population = sum(community_sample_sizes.values())

        community_clusters = {}
        for community in communities:
            name = community['name']
            population = community['size']
            community_clusters[name] = math.ceil(community_sample_sizes[name] / total_clusters)

        total_assigned_clusters = sum(community_clusters.values())
        if total_assigned_clusters != total_clusters:
            if total_assigned_clusters > total_clusters:
                excess_clusters = total_assigned_clusters - total_clusters
                while excess_clusters > 0:
                    name = random.choice(list(community_clusters.keys()))
                    if community_clusters[name] > 0:
                        community_clusters[name] -= 1
                        excess_clusters -= 1

            else:
                remaining_clusters = total_clusters - total_assigned_clusters
                remaining_population = total_sample_population - (
                        community_sample_sizes[name] * total_assigned_clusters)
                for i in range(remaining_clusters):
                    random_number = random.uniform(0, remaining_population)
                    for community in communities:
                        name = community['name']
                        population = community['size']
                        if random_number < population:
                            community_clusters[name] += 1
                            remaining_population -= population
                            break
                        random_number -= population
        # print(community_clusters)
        return community_clusters

    def assign_list_of_clusters(self,community_clusters):

        """
        Assigns a list of clusters to the `clusters` attribute of this object.

        Args:
            community_clusters (dict): A dictionary containing the number of clusters for each community.

        Returns:
            dict: A dictionary that maps each community to a list of cluster numbers. The keys of the dictionary are the
            same as the keys of `community_clusters`, and the values are lists of integers starting from 1 and ending with
            the number of clusters specified for each community.
        """

        # print(community_clusters)
        community_clusters_list = {}
        start_cluster = 1
        for name, num_clusters in community_clusters.items():
            cluster_numbers = list(range(start_cluster, start_cluster + num_clusters))
            start_cluster += num_clusters
            community_clusters_list[name] = cluster_numbers
        # print(community_clusters_list)
        self.clusters = community_clusters_list
        return community_clusters_list

    def get_clusters(self):
        if self.clusters is None:
            raise ValueError("Clusters not initialized")
        return self.clusters

    def check_clusters(self):
        for cluster_name in self.clusters:
            cluster_location = self.clusters[cluster_name]
            if len(cluster_location) > max_clusters_per_location:
                return data_display

    def start_calculation(self):
        community_sample_sizes = self.community_sample_sizes_calculation()
        community_clusters = self.assign_number_of_clusters(self.communities, community_sample_sizes,total_clusters)
        updated_community_clusters = self.assign_list_of_clusters(community_clusters)
        result = self.check_clusters()


if __name__ == '__main__':
    communities = [{'name': 'Community A', 'size': 1000},    {'name': 'Community B', 'size': 1500},
                   {'name': 'Community C','size': 2000}]

    clusterRandom = ClusterRandom(5, 95, None, None, 0, None, communities)
    clusterRandom.start_calculation()
    clusters = clusterRandom.get_clusters()
    print(clusters)

