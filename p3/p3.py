import os.path
from sys import platform
import random
import math
import numpy as np
import matplotlib.pyplot as plt

import p3.fox
import p3.memory_watcher
import p3.menu_manager
import p3.pad
import p3.state
import p3.state_manager
import p3.config as c
from p3.ANN import ANN as nnet

from math import sqrt

import array
import random
import json

from deap import base
from deap import creator
from deap import tools
from deap import algorithms
from deap.benchmarks.tools import diversity, convergence

random.seed(12345)

def find_dolphin_dir():
    """
    Attempts to find the dolphin user directory, if has
    been created on machine by opening up the dolphin 
    app.

    None on failure
    """

    
    if platform == "darwin": # macOS
        candidates = ['~/Library/Application Support/dolphin']
    elif platform == "linux" or platform == "linux2": # Linux
        candidates = ['~/.local/share/dolphin-emu']

    for candidate in candidates:
        path = os.path.expanduser(candidate)
        if os.path.isdir(path):
            return path
    return None

def write_locations(dolphin_dir, locations):
    """Writes out the locations list to the appropriate place under dolphin_dir."""
    path = dolphin_dir + '/MemoryWatcher/Locations.txt'
    with open(path, 'w') as f:
        f.write('\n'.join(locations))

        dolphin_dir = find_dolphin_dir()
        if dolphin_dir is None:
            print('Could not detect dolphin directory.')
            return

def run(fox, state, sm, mw, pad, pop, toolbox):
    mm = p3.menu_manager.MenuManager()
    while True:
        last_frame = state.frame
        res = next(mw)
        if res is not None:
            sm.handle(*res)
        if state.frame > last_frame:
            if not make_action(state, pad, mm, fox):
                break
    return

def make_action(state, pad, mm, fox):
    if state.menu == p3.state.Menu.Game:
        pad.release_button(p3.pad.Button.START)
        if fox.advance(state, pad, mm) == c.game['n_agents']:
            pad.reset()
            return False
    elif state.menu == p3.state.Menu.Characters:
        # print(state.players[0].cursor_x, state.players[0].cursor_y)
        mm.pick_fox(state, pad)
    elif state.menu == p3.state.Menu.Stages:
        mm.press_start_lots(state, pad)
    elif state.menu == p3.state.Menu.PostGame:
        mm.press_start_lots(state, pad)
    return True

# TRAINING PROCESS USING DEAP
def main():
    dolphin_dir = find_dolphin_dir()
    if dolphin_dir is None:
        print('Could not find dolphin config dir.')
        return

    state = p3.state.State()
    sm = p3.state_manager.StateManager(state)
    write_locations(dolphin_dir, sm.locations())

    fox = p3.fox.Fox()

    # Weights: (Minimize damage on self, Maximize damage dealt)
    creator.create("FitnessOptima", base.Fitness, weights = (-1.0, 1.0))
    creator.create("Individual", list, fitness = creator.FitnessOptima)
    # Create ranks and crowding distance here

    toolbox = base.Toolbox()

    BOUND_LOW, BOUND_UP = -1.0, 1.0
    NDIM = 30

    def uniform(low, up, size=None):
        try:
            return [random.uniform(a, b) for a, b in zip(low, up)]
        except TypeError:
            return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]

    toolbox.register("attr_real", random.uniform, -1, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_real, c.nnet['n_weights'])
    toolbox.register("population", tools.initRepeat, list, toolbox.individual, n = c.game['n_agents'])

    toolbox.register("evaluate", evalANN)

    toolbox.register("mate", tools.cxSimulatedBinaryBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0)
    toolbox.register("mutate", tools.mutPolynomialBounded, low=BOUND_LOW, up=BOUND_UP, eta=20.0, indpb=1.0/NDIM)
    toolbox.register("select", tools.selNSGA2)

    CXPB, MUTPB, NGEN = 0.9, 100, 2000

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    # stats.register("avg", numpy.mean, axis=0)
    # stats.register("std", numpy.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)
    
    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"

    pop = toolbox.population()

    # Add agents to the population
    for ind in pop:
        ann = nnet(c.nnet['n_inputs'], c.nnet['n_h_neurons'], c.nnet['n_outputs'], ind)
        fox.add_agent(ann)

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.evaluate(fox.agents)
    for ind, fit in zip(invalid_ind, fitnesses[0]):
        ind.fitness.values = tuple(fit)

    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    pop = toolbox.select(pop, len(pop))
    # print(logbook.stream)

    try:
        print('Start dolphin now. Press ^C to stop p3.')
        pad_path = dolphin_dir + '/Pipes/p3'
        mw_path = dolphin_dir + '/MemoryWatcher/MemoryWatcher'

        with p3.pad.Pad(pad_path) as pad, p3.memory_watcher.MemoryWatcher(mw_path) as mw:
            run(fox, state, sm, mw, pad, pop, toolbox)
        fitnesses = toolbox.evaluate(fox.agents)
        for ind, fit in zip(pop, fitnesses[0]):
            ind.fitness.values = tuple(fit)

        # Begin the generational process
        while fox.generation < NGEN:
            fox.generation += 1
            # fox.reset() # resets number of agents and agents list
            
            # offspring = tools.selTournamentDCD(pop, len(pop))  -- ASK TUTUM
            offspring = toolbox.select(pop, len(pop))
            offspring = [toolbox.clone(ind) for ind in offspring]

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() <= CXPB:
                    toolbox.mate(child1, child2)

                toolbox.mutate(child1)
                toolbox.mutate(child2)
                del child1.fitness.values, child2.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.evaluate(fox.agents)
            for ind, fit in zip(invalid_ind, fitnesses[0]):
                ind.fitness.values = fit
                # print(fit)

            # Select the next generation population
            pop = toolbox.select(offspring, len(offspring))
            record = stats.compile(pop)
            logbook.record(gen=fox.generation, evals=len(invalid_ind), **record)
            print(logbook.stream)

            fox.reset()
            for ind in offspring:
                ann = nnet(c.nnet['n_inputs'], c.nnet['n_h_neurons'], c.nnet['n_outputs'], ind)
                fox.add_agent(ann)

            with p3.pad.Pad(pad_path) as pad, p3.memory_watcher.MemoryWatcher(mw_path) as mw:
                run(fox, state, sm, mw, pad, offspring, toolbox)

            if (fox.generation % 50 == 0):
                statistics(pop, logbook, fox.generation)

        print("Training complete")

    except KeyboardInterrupt:        
        # np.savetxt('data.txt', data)
        # np.savetxt('last.txt', last)
        print('Stopped')

# print(__name__)
# if __name__ == '__main__':

# Fitness Evaluation:
def evalANN(agents):
    fits = []
    for a in agents:
        fits.append(a.fitness)
    return fits,
    # comma at the end is necessarys since DEAP stores fitness values as a tuple

def statistics(pop, logbook, gen):
    with open("zdt1_front.json") as optimal_front_data:
        optimal_front = json.load(optimal_front_data)
    # Use 500 of the 1000 points in the json file
    optimal_front = sorted(optimal_front[i] for i in range(0, len(optimal_front), 2))
    pop.sort(key=lambda x: x.fitness.values)
    
    # print(logbook)
    print("Convergence: ", convergence(pop, optimal_front))
    print("Diversity: ", diversity(pop, optimal_front[0], optimal_front[-1]))
    
    front = np.array([ind.fitness.values for ind in pop])
    optimal_front = np.array(optimal_front)
    # plt.scatter(optimal_front[:,0], optimal_front[:,1], c="r")
    plt.scatter(front[:,1], front[:,0], c="b")
    plt.axis("tight")
    plt.savefig("gen_" + str(gen) + ".png")
