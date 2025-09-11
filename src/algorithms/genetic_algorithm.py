"""Simple genetic algorithm to find optimal parameters for 2048 agents"""

from game.autoPlay import playGame
import random
import numpy as np
from typing import Tuple, List, Any, Callable
import logging 

logger = logging.getLogger("GeneticAlg")

def genetic_algorithm(
    initial_args: List[float],
    factory_function: Callable[[List[float]], Any],
    max_epochs: int = 10,
    population_size: int = 10,
    mutation_rate: float = 0.2,
    mutation_strength: float = 0.5,
    max_score:int = 2048
):
    # first game
    agent = factory_function(initial_args)
    best_score = playGame(agent)
    best_args = initial_args[:]

    for epoch in range(max_epochs):
        if best_score == max_score:
            logger.info("Model reached max score")
            break
            
        agents = mutate(
            best_args,
            factory_function,
            population_size,
            mutation_rate,
            mutation_strength,
        )

        for agent, args in agents:
            score = playGame(agent)
            if score > best_score:
                best_score = score
                best_args = args
        print(f"Epoch {epoch}: Best score = {best_score}, Args = {best_args}")

    return best_args, best_score


def mutate(
    args: List[float],
    factory_function: Callable[[List[float]], Any],
    number_of_creations: int,
    mutation_rate: float,
    mutation_strength: float,
) -> List[Tuple[Any, List[float]]]:
    agents = []

    for _ in range(number_of_creations):
        new_args = []
        for w in args:
            if random.random() < mutation_rate:
                w += np.random.normal(0, mutation_strength)
                w = max(0.0, w)
            new_args.append(w)

        agent = factory_function(new_args)
        agents.append((agent, new_args))

    return agents
