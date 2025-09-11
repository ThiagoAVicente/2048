from agents.expectedminimax import agent
from algorithms.genetic_algorithm import genetic_algorithm

initial_args = [0.1,0.2]

def create(args):
    return agent(w_empty=args[0],w_max=args[1])
    
print(genetic_algorithm(initial_args,create,))
