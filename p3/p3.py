import os.path
from sys import platform
import random
import math
import numpy as np

import p3.fox
import p3.memory_watcher
import p3.menu_manager
import p3.pad
import p3.state
import p3.state_manager
import p3.config as c
from p3.ANN import ANN as nnet

from deap import base
from deap import creator
from deap import tools
from deap import algorithms


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
        if fox.advance(state, pad, mm) == c.game['n_agents']:
            pad.reset()
            return False
    elif state.menu == p3.state.Menu.Characters:
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

    toolbox = base.Toolbox()

    toolbox.register("attr_real", random.uniform, -1, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_real, c.nnet['n_weights'])
    toolbox.register("population", tools.initRepeat, list, toolbox.individual, n = c.game['n_agents'])

    toolbox.register("evaluate", evalANN)

    toolbox.register("mate", tools.cxUniform, indpb = 0.5)
    toolbox.register("mutate", tools.mutGaussian, mu = 0, sigma = .25, indpb = 0.05)
    toolbox.register("select", tools.selNSGA2)

    CXPB, MUTPB, NGEN = 0.5, 0.2, 1000
    pop = toolbox.population()

    for ind in pop:
        ann = nnet(c.nnet['n_inputs'], c.nnet['n_h_neurons'], c.nnet['n_outputs'], ind)
        fox.add_agent(ann)

    data = []
    last = []

    # [0,0]
    # [[0,0]]

    try:
        print('Start dolphin now. Press ^C to stop p3.')
        pad_path = dolphin_dir + '/Pipes/p3'
        mw_path = dolphin_dir + '/MemoryWatcher/MemoryWatcher'
        with p3.pad.Pad(pad_path) as pad, p3.memory_watcher.MemoryWatcher(mw_path) as mw:
            run(fox, state, sm, mw, pad, pop, toolbox)

        fitnesses = list(toolbox.evaluate(fox, pop))[0]
        print("these are the fitnesses: ", fitnesses)
        for fit in fitnesses:
            temp = []
            temp.append(fit)
            fitnesses.append(temp)
        fitnesses.pop(0)

        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit[0]

        while fox.generation < NGEN:
            fox.generation += 1
            fox.reset()

            offspring = toolbox.select(pop, c.game['n_agents'])

            offspring = [toolbox.clone(ind) for ind in offspring]

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < MUTPB:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            for ind in offspring:
                ann = nnet(c.nnet['n_inputs'], c.nnet['n_h_neurons'], c.nnet['n_outputs'], ind)
                fox.add_agent(ann)

            with p3.pad.Pad(pad_path) as pad, p3.memory_watcher.MemoryWatcher(mw_path) as mw:
                run(fox, state, sm, mw, pad, offspring, toolbox)

            avg = 0
            fits = list(toolbox.evaluate(fox, offspring))
            for fit in fits[0]:
                temp = []
                temp.append(fit)
                fits.append(temp)
            fits.pop(0)

            temp = []
            for ind, fit in zip(offspring, fits):
                ind.fitness.values = fit
                temp.append(fit[0])
                avg += fit[0]
            temp.sort()

            avg /= c.game['n_agents']
            print("gen: ", fox.generation, " /  avg: ", avg, "best: ", temp[len(temp)-1])
            data.append(avg)
            temp.clear()
            last = offspring

            pop[:] = pop + offspring

        print("Training complete")
        np.savetxt('data.txt', data)
        np.savetxt('last.txt', last)
    except KeyboardInterrupt:        
        np.savetxt('data.txt', data)
        np.savetxt('last.txt', last)
        print('Stopped')

if __name__ == '__main__':
    main()


# Fitness Evaluation:
def evalANN(fox, individual):
    return fox.get_ind_fitness(individual),
    # comma at the end is necessarys since DEAP stores fitness values as a tuple
