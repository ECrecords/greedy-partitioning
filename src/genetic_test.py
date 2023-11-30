import random
import numpy as np
from deap import base, creator, tools

class VLSIPartitionGA:
    def __init__(self, signals, connections, n_partitions, pop_size):
        self.signals = signals
        self.connections = connections
        self.n_partitions = n_partitions
        self.pop_size = pop_size

        self.connectivity_matrix = self.create_connectivity_matrix()
        self.net_matrix = self.create_net_matrix()
        self.toolbox = base.Toolbox()
        self.setup_deap()

    def create_connectivity_matrix(self):
        matrix = np.zeros((len(self.signals), len(self.signals)), dtype=int)
        for src, dests in self.connections.items():
            for dest in dests:
                matrix[self.signals.index(src), self.signals.index(dest)] = 1
        return matrix

    def create_net_matrix(self):
        matrix = np.zeros((len(self.signals), len(self.signals)), dtype=int)
        for i, signal in enumerate(self.signals):
            if signal in self.connections:
                for dest in self.connections[signal]:
                    matrix[i, self.signals.index(dest)] = 1
                    matrix[self.signals.index(dest), i] = 1
        return matrix

    def initial_partitions(self, net_mat):
        modules = list(range(len(net_mat)))
        random.shuffle(modules)
        partitions = [[] for _ in range(self.n_partitions)]
        for i, module in enumerate(modules):
            partitions[i % self.n_partitions].append(module)
        return partitions

    def setup_deap(self):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        self.toolbox.register("partition", self.initial_partitions, net_mat=self.net_matrix)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.partition)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

    def create_population(self):
        return self.toolbox.population(n=self.pop_size)

    def display_matrices(self):
        print("Connectivity Matrix:\n", self.connectivity_matrix)
        print("\nNet Matrix:\n", self.net_matrix)

if __name__ == "__main__":
    # Usage
    signals = ["a", "b", "sel", "not_sel", "a_and_not_sel", "b_and_sel", "out"]
    connections = {
        "sel": ["not_sel", "b_and_sel"],
        "not_sel": ["a_and_not_sel"],
        "a": ["a_and_not_sel"],
        "b": ["b_and_sel"],
        "a_and_not_sel": ["out"],
        "b_and_sel": ["out"]
    }
    n_partitions = 3
    pop_size = 13

    ga = VLSIPartitionGA(signals, connections, n_partitions, pop_size)
    population = ga.create_population()
    ga.display_matrices()

    print("\nPopulation:")
    for individual in population:
        print(individual)
