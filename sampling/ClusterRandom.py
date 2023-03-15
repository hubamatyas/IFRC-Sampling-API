import math
import random

from sampling.SimpleRandom import SimpleRandom

total_clusters = 30


class ClusterRandom(SimpleRandom):
    def __init__(self, margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups,
                 communities):
        super().__init__(margin_of_error, confidence_level, individuals, households, non_response_rate, subgroups)
        self.communities = communities
        self.population_size = sum(communities.values())
        self.clusters = None

    def community_sample_sizes_calculation(self):
        community_sample_sizes = {}

        for community in self.communities:
            result = self.calculate_sample_size(self.communities[community], self.margin_of_error,
                                                self.confidence_level,
                                                self.non_response_rate)
            sample_size = result['total']
            community_sample_sizes[community] = sample_size

        # print(community_sample_sizes)
        return community_sample_sizes

    def assign_clusters(self, communities, community_sample_sizes):

        total_sample_population = sum(community_sample_sizes.values())

        community_clusters = {}
        for community, population in communities.items():
            community_clusters[community] = math.ceil(community_sample_sizes[community] / total_clusters)

        total_assigned_clusters = sum(community_clusters.values())
        if total_assigned_clusters != total_clusters:
            if total_assigned_clusters > total_clusters:
                excess_clusters = total_assigned_clusters - total_clusters
                while excess_clusters > 0:
                    community = random.choice(list(community_clusters.keys()))
                    if community_clusters[community] > 0:
                        community_clusters[community] -= 1
                        excess_clusters -= 1
            else:
                remaining_clusters = total_clusters - total_assigned_clusters
                remaining_population = total_sample_population - (
                        community_sample_sizes[community] * total_assigned_clusters)
                for i in range(remaining_clusters):
                    random_number = random.uniform(0, remaining_population)
                    for community, population in communities.items():
                        if random_number < population:
                            community_clusters[community] += 1
                            remaining_population -= population
                            break
                        random_number -= population

        start_cluster = 1
        for community, num_clusters in community_clusters.items():
            cluster_numbers = list(range(start_cluster, start_cluster + num_clusters))
            start_cluster += num_clusters
            community_clusters[community] = cluster_numbers

        self.clusters = community_clusters

    def get_clusters(self):
        if self.clusters is None:
            raise ValueError("Clusters not initialized")
        return self.clusters

# if __name__ == '__main__':
#     communities = {'A': 150, 'B': 500, 'C': 100, 'D': 350}
#     clusterRandom = ClusterRandom(5, 95, None, None, 0, None, communities)
#     community_sample_sizes = clusterRandom.community_sample_sizes_calculation()
#     clusterRandom.assign_clusters(communities, community_sample_sizes)
#     clusters = clusterRandom.get_clusters()
#     print(clusters)
