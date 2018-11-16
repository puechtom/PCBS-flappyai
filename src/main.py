from genetic import GeneticAlg

if __name__ == "__main__":
    ga = GeneticAlg()
    for i in range(5):
        ga.simulate()
        ga.mutate()
